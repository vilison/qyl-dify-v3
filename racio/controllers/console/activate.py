import random
from flask_restful import Resource, reqparse
from libs.helper import email, str_len, timezone
from libs.response import response_json
from models.racio.account import AccountStatus
from services.racio.account_service import AccountService
from services.dify.api_service import ApiService
from services.dify.account_service import AccountService as Dify_AccountService
from models.racio.account import Account, AccountRole
from . import api


class ActivateCheckApi(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True, nullable=False, location='json')
        args = parser.parse_args()

        token = args['token']
        invitation = AccountService.get_invitation_if_token_valid(token)

        tenant_name = ""
        role = ""
        if invitation is not None:
            if invitation['tenant']:
                tenant = invitation['tenant']
                tenant_name = tenant['name']

            member_invite = invitation['data']
            role = member_invite.role

        data = {'is_valid': invitation is not None, 'workspace_name': tenant_name if invitation else "", 'role': role}
        return response_json(0, 'success', data)


class ActivateApi(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True, nullable=False, location='json')
        # parser.add_argument('name', type=str_len(30), required=True, nullable=False, location='json')
        # parser.add_argument('password', type=valid_password, required=True, nullable=False, location='json')
        # parser.add_argument('interface_language', type=supported_language, required=True, nullable=False,location='json')
        # parser.add_argument('timezone', type=timezone, required=True, nullable=False, location='json')
        parser.add_argument('phone', type=str, required=True, nullable=True, location='json')
        # parser.add_argument('provider', type=str, required=True, nullable=False, location='json', default='wx')
        parser.add_argument('access_token', type=str, required=True, nullable=False, location='json', default='')
        parser.add_argument('code', type=str, required=True, nullable=True, location='json')
        parser.add_argument('tenant_name', type=str_len(255), required=True, nullable=True, location='json')
        args = parser.parse_args()

        # 获取登录openid
        access_data = AccountService.get_access_code(args['access_token'])
        if not access_data:
            return response_json(-1, '无授权信息，请重新登录授权')

        account_integrate = AccountService.get_account_integrate_by_openid(access_data['provider'],
                                                                           access_data['open_id'])

        if account_integrate is None:
            verify_data = AccountService.get_verify_code(args['token'])
            if not verify_data:
                return response_json(-1, '验证码已过期')

            if verify_data['phone'] != args['phone']:
                return response_json(-1, '验证手机号不正确')

            if verify_data['code'] != args['code']:
                return response_json(-1, '验证码不正确')

            AccountService.revoke_verify_code(args['token'])

        invitation = AccountService.get_invitation_if_token_valid(args['token'])
        if invitation is None:
            return response_json(-1, '该邀请已被使用')
        member_invite = invitation['data']
        tenant_id = member_invite.tenant_id
        AccountService.delete_member_invite(args['token'])
        apiService = ApiService()
        # 判断被邀请用户是否存在
        account_id = ''
        if account_integrate is None:
            name = ''
            email = ''
            # 创建账号
            for i in range(10):
                name = str(random.randint(100000000, 999999999))
                email = name + "@" + member_invite.domain
                account = Account.query.filter_by(email=email).first()
                if not account:
                    break
            account = apiService.create_account(name, email)
            if account is None:
                return response_json(-1, '激活失败，请重新获取邀请')
            account_id = account['id']
            apiService.account_update_status(account['id'], AccountStatus.ACTIVE)
            racio_account = AccountService.create_account(id=account['id'], email=account['email'],
                                                          name=account['name'],
                                                          interface_language=account['interface_language'],
                                                          phone=args['phone'], status=AccountStatus.ACTIVE)

        else:
            account_id = account_integrate.account_id
            racio_account = AccountService.get_account(account_id)

        if member_invite.role == AccountRole.OWNER:
            if args['tenant_name'] == '':
                return response_json(-1, '请填写空间名')
            #判断是否已创建owner空间
            is_exists = Dify_AccountService.check_owner_exists(account_id, AccountRole.OWNER)
            if is_exists:
                return response_json(-1, '该账号已创建空间，不能重复创建')
            # 创建空间
            tenant = apiService.create_tenant(args['tenant_name'], racio_account.email)
            tenant_id = tenant['id']
        else:
            # 加入空间
            apiService.create_tenant_member(tenant_id, account_id, member_invite.role)

        apiService.link_account_integrate(access_data['provider'], access_data['open_id'], account_id)
        AccountService.link_account_integrate(access_data['provider'], access_data['open_id'], racio_account)

        token = AccountService.get_account_jwt_token(racio_account)
        #切换用户空间
        Dify_AccountService.switch_tenant(token, tenant_id)
        data = {
            "token": token,
            "account_role": member_invite.role
        }
        return response_json(0, 'success', data)


class TestApi(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('account_id', type=str, required=True, nullable=False, location='json')
        parser.add_argument('role', type=str, required=True, nullable=False, location='json')
        args = parser.parse_args()

        data = Dify_AccountService.check_owner_exists(args['account_id'], args['role'])
        return response_json(0, 'success', data)


api.add_resource(ActivateCheckApi, '/activate/check')
api.add_resource(ActivateApi, '/activate')
api.add_resource(TestApi, '/activate/check_owner_exists')
