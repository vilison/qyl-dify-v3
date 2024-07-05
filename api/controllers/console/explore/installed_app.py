import uuid
from datetime import datetime, timezone

from flask_login import current_user
from flask_restful import Resource, inputs, marshal, marshal_with, reqparse
from sqlalchemy import and_
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, abort

from controllers.console import api
from controllers.console.explore.wraps import InstalledAppResource
from controllers.console.wraps import account_initialization_required, cloud_edition_billing_resource_check
from extensions.ext_database import db
from fields.installed_app_fields import installed_app_list_fields, installed_app_pagination_fields
from libs.login import login_required
from models.model import App, InstalledApp, RecommendedApp
from services.account_service import TenantService
from services.installed_app_service import InstalledAppService


class InstalledAppsListApi(Resource):
    @login_required
    @account_initialization_required
    @marshal_with(installed_app_list_fields)
    def get(self):
        current_tenant_id = current_user.current_tenant_id
        installed_apps = db.session.query(InstalledApp).filter(
            InstalledApp.tenant_id == current_tenant_id
        ).all()

        current_user.role = TenantService.get_user_role(current_user, current_user.current_tenant)
        installed_apps = [
            {
                'id': installed_app.id,
                'app': installed_app.app,
                'app_owner_tenant_id': installed_app.app_owner_tenant_id,
                'is_pinned': installed_app.is_pinned,
                'last_used_at': installed_app.last_used_at,
                'editable': current_user.role in ["owner", "admin"],
                'uninstallable': current_tenant_id == installed_app.app_owner_tenant_id
            }
            for installed_app in installed_apps
        ]
        installed_apps.sort(key=lambda app: (-app['is_pinned'],
                                             app['last_used_at'] is None,
                                             -app['last_used_at'].timestamp() if app['last_used_at'] is not None else 0))

        return {'installed_apps': installed_apps}

    @login_required
    @account_initialization_required
    @cloud_edition_billing_resource_check('apps')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('app_id', type=str, required=True, help='Invalid app_id')
        args = parser.parse_args()

        recommended_app = RecommendedApp.query.filter(RecommendedApp.app_id == args['app_id']).first()
        if recommended_app is None:
            raise NotFound('App not found')

        current_tenant_id = current_user.current_tenant_id
        app = db.session.query(App).filter(
            App.id == args['app_id']
        ).first()

        if app is None:
            raise NotFound('App not found')

        if not app.is_public:
            raise Forbidden('You can\'t install a non-public app')

        installed_app = InstalledApp.query.filter(and_(
            InstalledApp.app_id == args['app_id'],
            InstalledApp.tenant_id == current_tenant_id
        )).first()

        if installed_app is None:
            # todo: position
            recommended_app.install_count += 1

            new_installed_app = InstalledApp(
                app_id=args['app_id'],
                tenant_id=current_tenant_id,
                app_owner_tenant_id=app.tenant_id,
                is_pinned=False,
                last_used_at=datetime.now(timezone.utc).replace(tzinfo=None)
            )
            db.session.add(new_installed_app)
            db.session.commit()

        return {'message': 'App installed successfully'}


class InstalledAppsTagsListApi(Resource):
    @login_required
    @account_initialization_required
    def get(self):
        """Get installed apps with tags"""
        def uuid_list(value):
            try:
                return [str(uuid.UUID(v)) for v in value.split(',')]
            except ValueError:
                abort(400, message="Invalid UUID format in tag_ids.")
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=inputs.int_range(1, 99999), required=False, default=1, location='args')
        parser.add_argument('limit', type=inputs.int_range(1, 100), required=False, default=20, location='args')
        parser.add_argument('tag_ids', type=uuid_list, location='args', required=False)

        args = parser.parse_args()

        # get installed apps list with tags
        installed_app_service = InstalledAppService()
        installed_app_pagination = installed_app_service.get_paginate_installed_apps(current_user.current_tenant_id, args)
        if not installed_app_pagination:
            return {'data': [], 'total': 0, 'page': 1, 'limit': 20, 'has_more': False}

        return marshal(installed_app_pagination, installed_app_pagination_fields)


class InstalledAppApi(InstalledAppResource):
    """
    update and delete an installed app
    use InstalledAppResource to apply default decorators and get installed_app
    """
    def delete(self, installed_app):
        if installed_app.app_owner_tenant_id == current_user.current_tenant_id:
            raise BadRequest('You can\'t uninstall an app owned by the current tenant')

        db.session.delete(installed_app)
        db.session.commit()

        return {'result': 'success', 'message': 'App uninstalled successfully'}

    def patch(self, installed_app):
        parser = reqparse.RequestParser()
        parser.add_argument('is_pinned', type=inputs.boolean)
        args = parser.parse_args()

        commit_args = False
        if 'is_pinned' in args:
            installed_app.is_pinned = args['is_pinned']
            commit_args = True

        if commit_args:
            db.session.commit()

        return {'result': 'success', 'message': 'App info updated successfully'}


api.add_resource(InstalledAppsListApi, '/installed-apps')
api.add_resource(InstalledAppsTagsListApi, '/installed-apps/tags')
api.add_resource(InstalledAppApi, '/installed-apps/<uuid:installed_app_id>')
