import logging
from typing import Optional
from uuid import UUID

from flask import request
from flask_login import current_user
from flask_restful import Resource, fields, inputs, marshal, marshal_with, reqparse
from werkzeug.exceptions import BadRequest, Conflict, NotFound, Unauthorized

import services
from controllers.console import api
from controllers.console.admin import admin_required
from controllers.console.datasets.error import (
    FileTooLargeError,
    NoFileUploadedError,
    TooManyFilesError,
    UnsupportedFileTypeError,
)
from controllers.console.error import AccountNotLinkTenantError
from controllers.console.setup import setup_required
from controllers.console.wraps import account_initialization_required, cloud_edition_billing_resource_check
from events.tenant_event import tenant_was_created
from extensions.ext_database import db
from fields.member_fields import account_with_role_fields
from libs.helper import TimestampField
from libs.login import login_required
from models.account import Account, Tenant, TenantAccountJoin, TenantAccountJoinRole, TenantStatus
from services.account_service import TenantService
from services.file_service import FileService
from services.workspace_service import WorkspaceService

provider_fields = {
    'provider_name': fields.String,
    'provider_type': fields.String,
    'is_valid': fields.Boolean,
    'token_is_set': fields.Boolean,
}

tenant_fields = {
    'id': fields.String,
    'name': fields.String,
    'plan': fields.String,
    'status': fields.String,
    'created_at': TimestampField,
    'role': fields.String,
    'in_trial': fields.Boolean,
    'trial_end_reason': fields.String,
    'custom_config': fields.Raw(attribute='custom_config'),
}

tenants_fields = {
    'id': fields.String,
    'name': fields.String,
    'plan': fields.String,
    'status': fields.String,
    'created_at': TimestampField,
    'current': fields.Boolean
}

tenants_with_role_fields = {
    'id': fields.String,
    'name': fields.String,
    'plan': fields.String,
    'status': fields.String,
    'created_at': TimestampField,
    'role': fields.String
}

workspace_fields = {
    'id': fields.String,
    'name': fields.String,
    'status': fields.String,
    'created_at': TimestampField
}

tenant_account_join_fields = {
    'id': fields.String,
    'tenant_id': fields.String,
    'account_id': fields.String,
    'role': fields.String,
    'invited_by': fields.String,
    'created_at': TimestampField,
    'updated_at': TimestampField
}


class TenantListApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def get(self):
        tenants = TenantService.get_join_tenants(current_user)

        for tenant in tenants:
            if tenant.id == current_user.current_tenant_id:
                tenant.current = True  # Set current=True for current tenant
        return {'workspaces': marshal(tenants, tenants_fields)}, 200


class WorkspaceListApi(Resource):
    @setup_required
    @admin_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=inputs.int_range(1, 99999), required=False, default=1, location='args')
        parser.add_argument('limit', type=inputs.int_range(1, 100), required=False, default=20, location='args')
        args = parser.parse_args()

        tenants = db.session.query(Tenant).order_by(Tenant.created_at.desc())\
            .paginate(page=args['page'], per_page=args['limit'])

        has_more = False
        if len(tenants.items) == args['limit']:
            current_page_first_tenant = tenants.items[-1]
            rest_count = db.session.query(Tenant).filter(
                Tenant.created_at < current_page_first_tenant.created_at,
                Tenant.id != current_page_first_tenant.id
            ).count()

            if rest_count > 0:
                has_more = True
        total = db.session.query(Tenant).count()
        return {
            'data': marshal(tenants.items, workspace_fields),
            'has_more': has_more,
            'limit': args['limit'],
            'page': args['page'],
            'total': total
                }, 200

    @setup_required
    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        parser.add_argument('owner_email', type=str, required=True, location='json')

        args = parser.parse_args()
        name = args['name']
        owner_email = args['owner_email']

        # 400 - BAD REQUEST
        if not name:
            raise BadRequest('Missing name parameter.')
        if not owner_email:
            raise BadRequest('Missing owner_email parameter.')

        # 404 - NOT FOUND
        account = Account.query.filter_by(email=owner_email).first()
        if account is None:
            raise NotFound(f'Owner account {owner_email} not found.')

        try:
            tenant = TenantService.create_tenant(name)
            # add account as owner member
            TenantService.create_tenant_member(tenant, account, role='owner')
            # send event
            tenant_was_created.send(tenant)

            return {'data': marshal(tenant, workspace_fields)}, 201
        except Exception as e:
            logging.exception(f"An error occurred during the WorkspaceListApi.post() process with: {str(e)}")
            raise ValueError(str(e))


class WorkspaceApi(Resource):
    @setup_required
    @admin_required
    def get(self, workspace_id):
        workspace_id = str(workspace_id)
        tenant = Tenant.query.filter(Tenant.id == workspace_id).first()
        if not tenant:
            raise NotFound(f'Workspace {workspace_id} not found.')

        return {'data': marshal(tenant, workspace_fields)}, 200


class WorkspaceAccountMatchApi(Resource):
    @setup_required
    @admin_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('account_id', type=str, required=True,
                            location='args', help='Account_id is required.')
        parser.add_argument('role', type=str, required=False,
                            choices=['owner', 'admin', 'normal'],
                            default=TenantAccountJoinRole.OWNER.value,
                            location='args', help='Role is optional. Choose one of the following: owner, admin, normal.')

        args = parser.parse_args()
        account_id = args['account_id']
        role = args['role']

        # 400 - BAD REQUEST
        if not account_id:
            raise BadRequest('Missing account_id parameter.')
        if not role or role not in ['owner', 'admin', 'normal']:
            raise BadRequest('role parameter should be one of owner, admin or normal.')

        try:
            tenants = TenantAccountJoin.query.filter_by(account_id=UUID(str(account_id)), role=role).all()
            tenant_id_list = [tenant.tenant_id for tenant in tenants]

            return {'data': tenant_id_list}, 200
        except Exception as e:
            logging.exception(f"An error occurred during the WorkspaceAccountMatchApi.get() process with: {str(e)}")
            raise ValueError(str(e))


class WorkspaceAccountJoinApi(Resource):
    @setup_required
    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tenant_id', type=str, required=True, location='json', help='Tenant id is required.')
        parser.add_argument('account_id', type=str, required=True, location='json', help='Account id is required.')
        parser.add_argument('role', type=str, required=True,
                            choices=['owner', 'admin', 'normal'],
                            default=TenantAccountJoinRole.OWNER.value,
                            location='json', help='Role is required. choices: owner, admin, normal.')
        parser.add_argument('invited_by', type=str, required=False,
                            default=None, location='json', help='Invited by account id is required.')

        args = parser.parse_args()
        tenant_id = args['tenant_id']
        account_id = args['account_id']
        role = args['role']
        invited_by = args['invited_by']

        # 400 - BAD REQUEST
        if not tenant_id:
            raise BadRequest('Missing tenant_id parameter.')
        if not account_id:
            raise BadRequest('Missing account_id parameter.')
        if not role or role not in ['owner', 'admin', 'normal']:
            raise BadRequest('Missing role parameter. And it should be one of owner, admin or normal.')

        # 404 - NOT FOUND
        if tenant_id:
            self._check_tenant_by_id(tenant_id)
        if account_id:
            self._check_account_by_id(account_id)
        if invited_by:
            self._check_invited_by_id(invited_by)

        # 409 - Conflict
        ta = TenantAccountJoin.query.filter_by(tenant_id=tenant_id, account_id=account_id, role=role).first()
        if ta:
            raise Conflict(f'The Account {account_id} has been added into the tenant {tenant_id} already.')

        try:
            tenant_account_join = TenantAccountJoin(
                tenant_id=UUID(str(tenant_id)),
                account_id=UUID(str(account_id)),
                role=role,
                invited_by=UUID(str(invited_by)) if invited_by else None
            )
            db.session.add(tenant_account_join)
            db.session.commit()

            return {'data': marshal(tenant_account_join, tenant_account_join_fields)}, 201
        except Exception as e:
            logging.exception(f"An error occurred during the WorkspaceAccountJoinApi.post() process with: {str(e)}")
            raise ValueError(str(e))

    def _check_account_by_id(self, account_id: str) -> Optional[NotFound]:
        account = Account.query.filter_by(id=UUID(str(account_id))).first()
        if not account:
            raise NotFound(f'Account {account_id} not found.')
        else:
            return None

    def _check_tenant_by_id(self, tenant_id: str) -> Optional[NotFound]:
        tenant = Tenant.query.filter_by(id=UUID(str(tenant_id))).first()
        if not tenant:
            raise NotFound(f'Tenant {tenant_id} not found.')
        else:
            return None

    def _check_invited_by_id(self, invited_by: str) -> Optional[NotFound]:
        account = Account.query.filter_by(id=UUID(str(invited_by))).first()
        if not account:
            raise NotFound(f'Invited by Account {invited_by} not found.')
        else:
            return None


class WorkspaceAccountGetTenantsApi(Resource):
    @setup_required
    @admin_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('account_id', type=str, required=True, location='args', help='Account id is required.')

        args = parser.parse_args()
        account_id = args['account_id']

        # 400 - BAD REQUEST
        if not account_id:
            raise BadRequest('Missing account_id parameter.')

        # 404 - NOT FOUND
        account = Account.query.filter_by(id=UUID(str(account_id))).first()
        if not account:
            raise NotFound(f'Account {account_id} not found.')

        try:
            # Get all joined tenants
            tenants = TenantService.get_join_tenants(account)

            tenants_info = []
            for tenant in tenants:
                # Get role of tenant member
                tenant_account_join = db.session.query(TenantAccountJoin).filter(
                    TenantAccountJoin.tenant_id == tenant.id,
                    TenantAccountJoin.account_id == UUID(str(account_id))
                ).first()

                tenant_info = tenant.__dict__.copy()  # 复制所有属性
                if tenant_account_join:
                    role = tenant_account_join.role
                    tenant_info['role'] = role
                else:
                    tenant_info['role'] = None
                tenants_info.append(tenant_info)

            return {'data': marshal(tenants_info, tenants_with_role_fields)}, 200
        except Exception as e:
            logging.exception(f"An error occurred during the WorkspaceAccountGetTenantsApi.get() process with: {str(e)}")
            raise ValueError(str(e))


class WorkspaceAccountGetMembersApi(Resource):
    @setup_required
    @admin_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tenant_id', type=str, required=True, location='args', help='Tenant id is required.')

        args = parser.parse_args()
        tenant_id = args['tenant_id']

        # 400 - BAD REQUEST
        if not tenant_id:
            raise BadRequest('Missing tenant_id parameter.')

        # 404 - NOT FOUND
        tenant = Tenant.query.filter_by(id=UUID(str(tenant_id))).first()
        if not tenant:
            raise NotFound(f'Tenant {tenant_id} not found.')

        try:
            members = TenantService.get_tenant_members(tenant)

            return {'data': marshal(members, account_with_role_fields)}, 200
        except Exception as e:
            logging.exception(
                f"An error occurred during the WorkspaceAccountGetMembersApi.get() process with: {str(e)}")
            raise ValueError(str(e))


class TenantApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @marshal_with(tenant_fields)
    def get(self):
        if request.path == '/info':
            logging.warning('Deprecated URL /info was used.')

        tenant = current_user.current_tenant

        if tenant.status == TenantStatus.ARCHIVE:
            tenants = TenantService.get_join_tenants(current_user)
            # if there is any tenant, switch to the first one
            if len(tenants) > 0:
                TenantService.switch_tenant(current_user, tenants[0].id)
                tenant = tenants[0]
            # else, raise Unauthorized
            else:
                raise Unauthorized('workspace is archived')

        return WorkspaceService.get_tenant_info(tenant), 200


class SwitchWorkspaceApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tenant_id', type=str, required=True, location='json')
        args = parser.parse_args()

        # check if tenant_id is valid, 403 if not
        try:
            TenantService.switch_tenant(current_user, args['tenant_id'])
        except Exception:
            raise AccountNotLinkTenantError("Account not link tenant")

        new_tenant = db.session.query(Tenant).get(args['tenant_id'])  # Get new tenant

        return {'result': 'success', 'new_tenant': marshal(WorkspaceService.get_tenant_info(new_tenant), tenant_fields)}
    

class CustomConfigWorkspaceApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @cloud_edition_billing_resource_check('workspace_custom')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('remove_webapp_brand', type=bool, location='json')
        parser.add_argument('replace_webapp_logo', type=str,  location='json')
        args = parser.parse_args()

        custom_config_dict = {
            'remove_webapp_brand': args['remove_webapp_brand'],
            'replace_webapp_logo': args['replace_webapp_logo'],
        }

        tenant = db.session.query(Tenant).filter(Tenant.id == current_user.current_tenant_id).one_or_404()

        tenant.custom_config_dict = custom_config_dict
        db.session.commit()

        return {'result': 'success', 'tenant': marshal(WorkspaceService.get_tenant_info(tenant), tenant_fields)}
    

class WebappLogoWorkspaceApi(Resource):
    @setup_required
    @login_required
    @account_initialization_required
    @cloud_edition_billing_resource_check('workspace_custom')
    def post(self):
        # get file from request
        file = request.files['file']

        # check file
        if 'file' not in request.files:
            raise NoFileUploadedError()

        if len(request.files) > 1:
            raise TooManyFilesError()

        extension = file.filename.split('.')[-1]
        if extension.lower() not in ['svg', 'png']:
            raise UnsupportedFileTypeError()

        try:
            upload_file = FileService.upload_file(file, current_user, True)

        except services.errors.file.FileTooLargeError as file_too_large_error:
            raise FileTooLargeError(file_too_large_error.description)
        except services.errors.file.UnsupportedFileTypeError:
            raise UnsupportedFileTypeError()
        
        return {'id': upload_file.id}, 201


api.add_resource(TenantListApi, '/workspaces')  # GET for getting all tenants
api.add_resource(WorkspaceListApi, '/all-workspaces')  # GET for getting all tenants via admin
api.add_resource(WorkspaceApi, '/all-workspaces/<uuid:workspace_id>')  # GET for tenant by id via admin
api.add_resource(WorkspaceAccountMatchApi, '/all-workspaces/match-account')  # GET for tenant by account and role via admin
api.add_resource(WorkspaceAccountJoinApi, '/all-workspaces/add-member')  # POST for joining tenant by account via admin
api.add_resource(WorkspaceAccountGetTenantsApi, '/all-workspaces/get-tenants')  # GET for getting all tenants by account id via admin
api.add_resource(WorkspaceAccountGetMembersApi, '/all-workspaces/get-members')  # GET for getting all accounts by tenant id via admin

api.add_resource(TenantApi, '/workspaces/current', endpoint='workspaces_current')  # GET for getting current tenant info
api.add_resource(TenantApi, '/info', endpoint='info')  # Deprecated
api.add_resource(SwitchWorkspaceApi, '/workspaces/switch')  # POST for switching tenant
api.add_resource(CustomConfigWorkspaceApi, '/workspaces/custom-config')
api.add_resource(WebappLogoWorkspaceApi, '/workspaces/custom-config/webapp-logo/upload')
