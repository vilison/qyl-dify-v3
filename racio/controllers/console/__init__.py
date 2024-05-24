from flask import Blueprint

from libs.external_api import ExternalApi

bp = Blueprint('console', __name__, url_prefix='/console')
api = ExternalApi(bp)


from . import activate, sms, oauth, account

