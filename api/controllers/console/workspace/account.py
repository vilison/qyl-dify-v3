import datetime
import logging
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

import pytz
from flask import current_app, request
from flask_login import current_user
from flask_restful import Resource, fields, marshal, marshal_with, reqparse
from werkzeug.exceptions import BadRequest, Conflict, NotFound

from constants.languages import languages, supported_language
from controllers.console import api
from controllers.console.admin import admin_required
from controllers.console.setup import setup_required
from controllers.console.workspace.error import (
    AccountAlreadyInitedError,
    CurrentPasswordIncorrectError,
    InvalidInvitationCodeError,
    RepeatPasswordNotMatchError,
)
from controllers.console.wraps import account_initialization_required
from extensions.ext_database import db
from fields.member_fields import account_fields
from libs.helper import TimestampField, timezone
from libs.login import login_required
from models.account import Account, AccountIntegrate, AccountStatus, InvitationCode
from services.account_service import AccountService, RegisterService
from services.errors.account import CurrentPasswordIncorrectError as ServiceCurrentPasswordIncorrectError


@dataclass
class UserInfo:
    # id: str
    name: str
    email: str


@dataclass
class OAuthUserInfo:
    provider: str
    open_id: str


class AccountsListApi(Resource):
    @setup_required
    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json', help='Name is required.')
        parser.add_argument('email', type=str, required=True, location='json', help='Email is required.')
        # parser.add_argument('provider', type=str, required=True, location='json', help='Provider is required.')
        # parser.add_argument('open_id', type=str, required=True, location='json', help='Open_id is required.')

        args = parser.parse_args()
        name = args['name']
        email = args['email']
        # provider = args['provider']
        # open_id = args['open_id']

        # 400 - BAD REQUEST
        if not name:
            raise BadRequest('Missing name parameter.')
        if not email:
            raise BadRequest('Missing email parameter.')
        # if not provider:
        #     raise BadRequest('Missing provider parameter.')
        # if not open_id:
        #     raise BadRequest('Missing open_id parameter.')

        # 409 - Conflict - Get account by email.
        user_info = UserInfo(
            name=name,
            email=email
        )
        account = self._get_account_by_email(user_info)
        if account:
            raise Conflict('Account with email already exists.')

        # # 409 - Conflict - Get account by openid.
        # oauth_user_info = OAuthUserInfo(
        #     provider=provider,
        #     open_id=open_id
        # )
        # account = self._get_account_by_openid(oauth_user_info)
        # if account:
        #     raise Conflict('Account with open_id already exists.')

        # 201 - Create
        try:
            account = self._generate_account_by_email(user_info)

            # if account.status == AccountStatus.PENDING.value:
            #     account.status = AccountStatus.ACTIVE.value
            #     account.initialized_at = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
            #     db.session.commit()

            return {'data': marshal(account, account_fields)}, 201
        except Exception as e:
            logging.exception(
                f"An error occurred during the AccountsListApi._generate_account process with: {str(e)}")
            raise ValueError(str(e))

    def _get_account_by_openid(self, oauth_user_info: OAuthUserInfo) -> Optional[Account]:
        account = Account.get_by_openid(oauth_user_info.provider, oauth_user_info.open_id)
        return account

    def _get_account_by_email(self, user_info: UserInfo) -> Optional[Account]:
        account = Account.query.filter_by(email=user_info.email).first()
        return account

    def _generate_account(self, user_info: UserInfo, oauth_user_info: OAuthUserInfo) -> Optional[Account]:
        # Create account
        account = RegisterService.register(
            name=user_info.name,
            email=user_info.email,
            password=None,
            provider=oauth_user_info.provider,
            open_id=oauth_user_info.open_id
        )

        # Set interface language
        preferred_lang = request.accept_languages.best_match(languages)
        if preferred_lang and preferred_lang in languages:
            interface_language = preferred_lang
        else:
            interface_language = languages[0]
        account.interface_language = interface_language
        db.session.commit()

        # Link account
        AccountService.link_account_integrate(oauth_user_info.provider, oauth_user_info.open_id, account)

        return account

    def _generate_account_by_email(self, user_info: UserInfo) -> Optional[Account]:
        # Create account
        account = RegisterService.register(
            name=user_info.name,
            email=user_info.email,
            password=None,
            status=AccountStatus.PENDING
        )

        # Set interface language
        preferred_lang = request.accept_languages.best_match(languages)
        if preferred_lang and preferred_lang in languages:
            interface_language = preferred_lang
        else:
            interface_language = languages[0]
        account.interface_language = interface_language
        db.session.commit()

        return account


class AccountsApi(Resource):
    @setup_required
    @admin_required
    def get(self, account_id):
        account = Account.query.get(UUID(str(account_id)))
        if not account:
            raise NotFound(f'Account {account_id} not found.')

        return {'data': marshal(account, account_fields)}, 200


class AccountsStatusApi(Resource):
    @setup_required
    @admin_required
    def put(self, account_id):
        # 400
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=AccountStatus, required=True, location='json')
        args = parser.parse_args()
        new_status = args['status']
        if new_status not in AccountStatus:
            raise BadRequest(f'Invalid status {new_status}')

        # todo: 403

        # 404
        account = Account.query.get(UUID(str(account_id)))
        if not account:
            raise NotFound(f'Account {account_id} not found.')

        try:
            updated_account = AccountService.update_account(account, status=new_status)
            return {'result': 'success'}, 200
        except Exception as e:
            raise ValueError(str(e))


class AccountsVerifyEmailApi(Resource):
    @setup_required
    @admin_required
    def get(self):
        # 400
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, location='args', help='email is required.')
        args = parser.parse_args()
        email = args['email']
        if not email:
            raise BadRequest('Missing email parameter.')

        account = Account.query.filter(Account.email == email).first()
        result = account is not None

        return {'data': {'email': email, 'result': result}}, 200


class AccountIntegratesListApi(Resource):
    @setup_required
    @admin_required
    def post(self):
        # 400
        parser = reqparse.RequestParser()
        parser.add_argument('open_id', type=str, required=True, location='json', help='open_id is required.')
        parser.add_argument('provider', type=str, required=True, location='json', help='provider is required.')
        parser.add_argument('account_id', type=str, required=True, location='json', help='account_id is required.')
        args = parser.parse_args()
        open_id = args['open_id']
        provider = args['provider']
        account_id = args['account_id']
        if not open_id:
            raise BadRequest('Missing open_id parameter.')
        if not provider:
            raise BadRequest('Missing provider parameter.')
        if not account_id:
            raise BadRequest('Missing account_id parameter.')

        # 403
        account = Account.query.get(UUID(str(account_id)))
        if not account:
            raise NotFound(f'Account {account_id} not found.')

        try:
            # Query whether there is an existing binding record for the same provider and open_id
            account_integrate: Optional[AccountIntegrate] = AccountIntegrate.query.filter_by(
                account_id=UUID(str(account_id)),
                provider=provider,
                open_id=open_id).first()
            if account_integrate:
                return {'data': {'result': True}}, 200
            else:
                # create new linked account with provider and open_id
                AccountService.link_account_integrate(provider, open_id, account)
                return {'data': {'result': True}}, 201
        except Exception as e:
            raise ValueError(str(e))


class AccountIntegratesVerifyOpenIdApi(Resource):
    @setup_required
    @admin_required
    def get(self):
        # 400
        parser = reqparse.RequestParser()
        parser.add_argument('open_id', type=str, required=True, location='args', help='open_id is required.')
        parser.add_argument('provider', type=str, required=True, location='args', help='provider is required.')
        parser.add_argument('account_id', type=str, required=True, location='args', help='account_id is required.')
        args = parser.parse_args()
        open_id = args['open_id']
        provider = args['provider']
        account_id = args['account_id']
        if not open_id:
            raise BadRequest('Missing open_id parameter.')
        if not provider:
            raise BadRequest('Missing provider parameter.')
        if not account_id:
            raise BadRequest('Missing account_id parameter.')

        try:
            result = False
            # Query whether there is an existing binding record for the same provider and open_id
            account_integrate: Optional[AccountIntegrate] = AccountIntegrate.query.filter_by(
                account_id=UUID(str(account_id)),
                provider=provider,
                open_id=open_id).first()
            if account_integrate:
                result = True

            return {'data': {'open_id': open_id, 'provider': provider, 'account_id': account_id, 'result': result}}, 200
        except Exception as e:
            raise ValueError(str(e))


class AccountInitApi(Resource):

    @setup_required
    @login_required
    def post(self):
        account = current_user

        if account.status == 'active':
            raise AccountAlreadyInitedError()

        parser = reqparse.RequestParser()

        if current_app.config['EDITION'] == 'CLOUD':
            parser.add_argument('invitation_code', type=str, location='json')

        parser.add_argument(
            'interface_language', type=supported_language, required=True, location='json')
        parser.add_argument('timezone', type=timezone,
                            required=True, location='json')
        args = parser.parse_args()

        if current_app.config['EDITION'] == 'CLOUD':
            if not args['invitation_code']:
                raise ValueError('invitation_code is required')

            # check invitation code
            invitation_code = db.session.query(InvitationCode).filter(
                InvitationCode.code == args['invitation_code'],
                InvitationCode.status == 'unused',
            ).first()

            if not invitation_code:
                raise InvalidInvitationCodeError()

            invitation_code.status = 'used'
            invitation_code.used_at = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
            invitation_code.used_by_tenant_id = account.current_tenant_id
            invitation_code.used_by_account_id = account.id

        account.interface_language = args['interface_language']
        account.timezone = args['timezone']
        account.interface_theme = 'light'
        account.status = 'active'
        account.initialized_at = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
        db.session.commit()

        return {'result': 'success'}


class AccountProfileApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @marshal_with(account_fields)
    def get(self):
        return current_user


class AccountNameApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @marshal_with(account_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args()

        # Validate account name length
        if len(args['name']) < 3 or len(args['name']) > 30:
            raise ValueError(
                "Account name must be between 3 and 30 characters.")

        updated_account = AccountService.update_account(current_user, name=args['name'])

        return updated_account


class AccountAvatarApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @marshal_with(account_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('avatar', type=str, required=True, location='json')
        args = parser.parse_args()

        updated_account = AccountService.update_account(current_user, avatar=args['avatar'])

        return updated_account


class AccountInterfaceLanguageApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @marshal_with(account_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'interface_language', type=supported_language, required=True, location='json')
        args = parser.parse_args()

        updated_account = AccountService.update_account(current_user, interface_language=args['interface_language'])

        return updated_account


class AccountInterfaceThemeApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @marshal_with(account_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('interface_theme', type=str, choices=[
            'light', 'dark'], required=True, location='json')
        args = parser.parse_args()

        updated_account = AccountService.update_account(current_user, interface_theme=args['interface_theme'])

        return updated_account


class AccountTimezoneApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @marshal_with(account_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('timezone', type=str,
                            required=True, location='json')
        args = parser.parse_args()

        # Validate timezone string, e.g. America/New_York, Asia/Shanghai
        if args['timezone'] not in pytz.all_timezones:
            raise ValueError("Invalid timezone string.")

        updated_account = AccountService.update_account(current_user, timezone=args['timezone'])

        return updated_account


class AccountPasswordApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @marshal_with(account_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str,
                            required=False, location='json')
        parser.add_argument('new_password', type=str,
                            required=True, location='json')
        parser.add_argument('repeat_new_password', type=str,
                            required=True, location='json')
        args = parser.parse_args()

        if args['new_password'] != args['repeat_new_password']:
            raise RepeatPasswordNotMatchError()

        try:
            AccountService.update_account_password(
                current_user, args['password'], args['new_password'])
        except ServiceCurrentPasswordIncorrectError:
            raise CurrentPasswordIncorrectError()

        return {"result": "success"}


class AccountIntegrateApi(Resource):
    integrate_fields = {
        'provider': fields.String,
        'created_at': TimestampField,
        'is_bound': fields.Boolean,
        'link': fields.String
    }

    integrate_list_fields = {
        'data': fields.List(fields.Nested(integrate_fields)),
    }

    @setup_required
    @login_required
    @account_initialization_required
    @marshal_with(integrate_list_fields)
    def get(self):
        account = current_user

        account_integrates = db.session.query(AccountIntegrate).filter(
            AccountIntegrate.account_id == account.id).all()

        base_url = request.url_root.rstrip('/')
        oauth_base_path = "/console/api/oauth/login"
        providers = ["github", "google", "wechat"]

        integrate_data = []
        for provider in providers:
            existing_integrate = next((ai for ai in account_integrates if ai.provider == provider), None)
            if existing_integrate:
                integrate_data.append({
                    'id': existing_integrate.id,
                    'provider': provider,
                    'created_at': existing_integrate.created_at,
                    'is_bound': True,
                    'link': None
                })
            else:
                integrate_data.append({
                    'id': None,
                    'provider': provider,
                    'created_at': None,
                    'is_bound': False,
                    'link': f'{base_url}{oauth_base_path}/{provider}'
                })

        return {'data': integrate_data}


# Register API resources
api.add_resource(AccountsListApi, '/accounts')  # POST new account via admin
api.add_resource(AccountsApi, '/accounts/<uuid:account_id>')  # GET for account by id via admin
api.add_resource(AccountsStatusApi, '/accounts/<uuid:account_id>/update-status')  # PATCH for account status by id via admin
api.add_resource(AccountsVerifyEmailApi, '/accounts/verify-email')  # GET for verification email via admin
api.add_resource(AccountIntegratesListApi, '/account-integrates')  # POST new accountIntegrate via admin
api.add_resource(AccountIntegratesVerifyOpenIdApi, '/account-integrates/verify-openid')  # GET for verification openId via admin
api.add_resource(AccountInitApi, '/account/init')
api.add_resource(AccountProfileApi, '/account/profile')
api.add_resource(AccountNameApi, '/account/name')
api.add_resource(AccountAvatarApi, '/account/avatar')
api.add_resource(AccountInterfaceLanguageApi, '/account/interface-language')
api.add_resource(AccountInterfaceThemeApi, '/account/interface-theme')
api.add_resource(AccountTimezoneApi, '/account/timezone')
api.add_resource(AccountPasswordApi, '/account/password')
api.add_resource(AccountIntegrateApi, '/account/integrates')
# api.add_resource(AccountEmailApi, '/account/email')
# api.add_resource(AccountEmailVerifyApi, '/account/email-verify')
