import logging

from flask import current_app, g
from flask_login import current_user
from libs.login import login_required
from services.racio.account_service import AccountService
from models.racio.account import Account, AccountRole
from flask_restful import Resource, reqparse, inputs, marshal
from libs.helper import email
from libs.response import response_json
from libs.email import send_invite_member_mail
from . import api
from services.errors.account import AccountAlreadyInTenantError
from fields.app_fields import (
    member_invites_fields,
)


class MemberInviteListApi(Resource):

    @login_required
    def post(self):
        """Get account list"""
        parser = reqparse.RequestParser()
        parser.add_argument('tenant_id', type=str, required=False, default='', location='json')
        args = parser.parse_args()

        tenant_id = None
        if args['tenant_id'] != '':
            tenant_id = args['tenant_id']
        member_invites = AccountService.get_member_invites(tenant_id)
        return response_json(0, 'success', marshal(member_invites, member_invites_fields))


class MemberInviteEmailApi(Resource):
    """Invite a new member by email."""

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=False, location='json')
        parser.add_argument('domain', type=str, required=True, location='json', default='')
        parser.add_argument('role', type=str, required=True, location='json', default='')
        parser.add_argument('tenant_id', type=str, required=True, location='json', default='')
        parser.add_argument('remark', type=str, location='json', default='')
        args = parser.parse_args()

        if current_user.account_role == AccountRole.SUPERADMIN:
            if args['role'] != AccountRole.OWNER:
                response_json(-1, '超级管理员只能邀请空间所有者')
        else:
            if current_user.account_role == AccountRole.OWNER:
                if args['role'] == AccountRole.OWNER:
                    response_json(-1, '空间所有者不能邀请空间所有者')

            if current_user.account_role == AccountRole.ADMIN:
                if args['role'] != AccountRole.NORMAL:
                    response_json(-1, '管理员只能邀请普通用户')

        invitee_email = ''
        send_flag = False
        if args['email'] != '':
            try:
                invitee_email = email(args['email'])
                send_flag = True
            except Exception as e:
                logging.info(str(e))

        tenant_id = None
        if args['tenant_id'] != '':
            tenant_id = args['tenant_id']

        invitation_result = {}
        console_web_url = current_app.config.get("CONSOLE_WEB_URL")
        try:
            member_invite = AccountService.create_member_invite(tenant_id, args['role'], current_user.id,
                                                                args['remark'], args['domain'])
            if send_flag:
                # send email
                send_invite_member_mail(
                    language=current_user.interface_language,
                    to=invitee_email,
                    token=member_invite.id,
                    inviter_name='Racio',
                )
            invitation_result = {
                'status': 'success',
                'email': invitee_email,
                'url': f'{console_web_url}/activate?token={member_invite.id}'
            }
        except AccountAlreadyInTenantError:
            invitation_result = {
                'status': 'success',
                'email': invitee_email,
                'url': f'{console_web_url}/signin'
            }
        except Exception as e:
            invitation_result = {
                'status': 'failed',
                'email': invitee_email,
                'message': str(e)
            }
        return response_json(0, 'success', invitation_result)


api.add_resource(MemberInviteListApi, '/member_invites')
api.add_resource(MemberInviteEmailApi, '/member_invites/invite-email')
