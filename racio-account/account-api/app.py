import os
import sys
from logging.handlers import RotatingFileHandler

if not os.environ.get("DEBUG") or os.environ.get("DEBUG").lower() != 'true':
    from gevent import monkey

    monkey.patch_all()


import json
import logging
import threading
import time
import warnings

from flask import Flask, Response, request, g
from flask_cors import CORS
from werkzeug.exceptions import Unauthorized
from config import Config


# DO NOT REMOVE BELOW
from extensions import (
    # ext_celery,
    ext_compress,
    ext_database,
    ext_login,
    ext_migrate,
    ext_redis,
    ext_mail,
    ext_sms
)
from extensions.ext_database import db
from extensions.ext_login import login_manager
from libs.passport import PassportService
from services.racio.account_service import AccountService
# from services.racio.oauth2_service import config_oauth

# DO NOT REMOVE ABOVE


warnings.simplefilter("ignore", ResourceWarning)

# fix windows platform
if os.name == "nt":
    os.system('tzutil /s "UTC"')
else:
    os.environ['TZ'] = 'UTC'
    time.tzset()


class AccountApp(Flask):
    pass


# -------------
# Configuration
# -------------


# ----------------------------
# Application Factory Function
# ----------------------------


def create_app(test_config=None) -> Flask:
    app = AccountApp(__name__)

    app.config.from_object(Config())

    app.secret_key = app.config['SECRET_KEY']

    log_handlers = None
    log_file = app.config.get('LOG_FILE')
    if log_file:
        log_dir = os.path.dirname(log_file)
        os.makedirs(log_dir, exist_ok=True)
        log_handlers = [
            RotatingFileHandler(
                filename=log_file,
                maxBytes=1024 * 1024 * 1024,
                backupCount=5
            ),
            logging.StreamHandler(sys.stdout)
        ]
    logging.basicConfig(
        level=app.config.get('LOG_LEVEL'),
        format=app.config.get('LOG_FORMAT'),
        datefmt=app.config.get('LOG_DATEFORMAT'),
        handlers=log_handlers
    )

    initialize_extensions(app)

    # Create tables if they do not exist already
    # with app.app_context():
    #     try:
    #         db.session.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    #         db.session.commit()
    #     except Exception as e:
    #         logging.info("uuid-ossp 已存在")
    #     db.create_all()

    # config_oauth(app)
    register_blueprints(app)

    return app


def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)

    ext_compress.init_app(app)
    ext_database.init_app(app)
    ext_migrate.init(app, db)
    ext_redis.init_app(app)
    # ext_celery.init_app(app)
    ext_login.init_app(app)
    ext_mail.init_app(app)
    ext_sms.init_app(app)


# Flask-Login configuration
@login_manager.request_loader
def load_user_from_request(request_from_flask_login):
    """Load user based on the request."""
    if request.blueprint in ['console', 'web']:
        # Check if the user_id contains a dot, indicating the old format
        auth_header = request.headers.get('Authorization', '')
        if not auth_header:
            auth_token = request.args.get('_token')
            if not auth_token:
                raise Unauthorized('Invalid Authorization token.')
        else:
            if ' ' not in auth_header:
                raise Unauthorized('Invalid Authorization header format. Expected \'Bearer <api-key>\' format.')
            auth_scheme, auth_token = auth_header.split(None, 1)
            auth_scheme = auth_scheme.lower()
            if auth_scheme != 'bearer':
                raise Unauthorized('Invalid Authorization header format. Expected \'Bearer <api-key>\' format.')

        decoded = PassportService().verify(auth_token)
        user_id = decoded.get('user_id')
        # g.auth_token = auth_token
        setattr(g, 'auth_token', auth_token)
        account = AccountService.load_user(user_id)
        return account
    else:
        return None


@login_manager.unauthorized_handler
def unauthorized_handler():
    """Handle unauthorized requests."""
    return Response(json.dumps({
        'code': 'unauthorized',
        'message': "Unauthorized."
    }), status=401, content_type="application/json")


# register blueprint routers
def register_blueprints(app):
    from controllers.console import bp as console_app_bp
    from controllers.web import bp as web_app_bp

    CORS(console_app_bp,
         resources={
             r"/*": {"origins": app.config['CONSOLE_CORS_ALLOW_ORIGINS']}},
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'PATCH'],
         expose_headers=['X-Version', 'X-Env']
         )

    app.register_blueprint(console_app_bp)

    CORS(web_app_bp,
         resources={
             r"/*": {"origins": app.config['CONSOLE_CORS_ALLOW_ORIGINS']}},
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'PATCH'],
         expose_headers=['X-Version', 'X-Env']
         )

    app.register_blueprint(web_app_bp)



# create app
app = create_app()
# CORS(app)
# celery = app.extensions["celery"]

if app.config['TESTING']:
    print("App is running in TESTING mode")


@app.after_request
def after_request(response):
    """Add Version headers to the response."""
    response.set_cookie('remember_token', '', expires=0)
    response.headers.add('X-Version', app.config['CURRENT_VERSION'])
    response.headers.add('X-Env', app.config['DEPLOY_ENV'])
    return response


@app.route('/health')
def health():
    return Response(json.dumps({
        'status': 'ok',
        'version': app.config['CURRENT_VERSION']
    }), status=200, content_type="application/json")


@app.route('/threads')
def threads():
    num_threads = threading.active_count()
    threads = threading.enumerate()

    thread_list = []
    for thread in threads:
        thread_name = thread.name
        thread_id = thread.ident
        is_alive = thread.is_alive()

        thread_list.append({
            'name': thread_name,
            'id': thread_id,
            'is_alive': is_alive
        })

    return {
        'thread_num': num_threads,
        'threads': thread_list
    }


@app.route('/db-pool-stat')
def pool_stat():
    engine = db.engine
    return {
        'pool_size': engine.pool.size(),
        'checked_in_connections': engine.pool.checkedin(),
        'checked_out_connections': engine.pool.checkedout(),
        'overflow_connections': engine.pool.overflow(),
        'connection_timeout': engine.pool.timeout(),
        'recycle_time': db.engine.pool._recycle
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
