from flask_login import current_user
from flask_restful import marshal, Resource, reqparse
from libs.response import response_json
from services.dify.api_service import ApiService
from services.racio.account_service import AccountService
from libs.login import login_required
from . import api
from fields.app_fields import (
    account_partial_fields,
)


class MemberListApi(Resource):
    @login_required
    def post(self):
        apiService = ApiService()
        datas = apiService.get_members()
        if not datas:
            return response_json(-1, '暂无数据')
        members = []
        for member in datas:
            racio_account = AccountService.get_account(member['id'])
            if racio_account:
                racio_account.account_role = member['role']
                members.append(racio_account)
        return response_json(0, 'success', marshal(members, account_partial_fields))


class MemberRemoveApi(Resource):
    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('account_id', type=str, required=True, location='json')
        args = parser.parse_args()

        apiService = ApiService()
        result = apiService.member_cancel_invite(args['account_id'])
        if not result:
            return response_json(-1, '移除失败')
        return response_json(0, 'success')


class MemberUpdateRoleApi(Resource):
    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('account_id', type=str, required=True, location='json')
        parser.add_argument('role', type=str, required=True, location='json')
        args = parser.parse_args()

        apiService = ApiService()
        result = apiService.member_update_role(args['account_id'], args['role'])
        if not result:
            return response_json(-1, '变更失败')
        return response_json(0, 'success')


api.add_resource(MemberListApi, '/members')
api.add_resource(MemberRemoveApi, '/member/remove')
api.add_resource(MemberUpdateRoleApi, '/members/update_role')
