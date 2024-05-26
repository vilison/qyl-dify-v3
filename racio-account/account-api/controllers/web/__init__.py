from flask import Blueprint

from libs.external_api import ExternalApi

bp = Blueprint('web', __name__, url_prefix='/web')
api = ExternalApi(bp)

from . import login, account, tenant, member_invite, member, init
# from . import oauth