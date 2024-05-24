import json
import logging

import requests
from flask import g, current_app


class ApiService:
    DIFY_API_URL = ''

    TOKEN = ''
    ADMIN_API_KEY = ''
    admin_request_headers = {}
    user_request_headers = {}

    def __init__(self):

        self.TOKEN = getattr(g, 'auth_token', "")
        with current_app.app_context():
            self.DIFY_API_URL = current_app.config.get('DIFY_API_URL')
            self.ADMIN_API_KEY = current_app.config.get('DIFY_ADMIN_API_KEY')

        self.admin_request_headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Authorization': 'Bearer '+self.ADMIN_API_KEY
        }
        self.user_request_headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Authorization': 'Bearer '+self.TOKEN
        }

    '''
    获取空间信息接口
    响应
    {
        "data": {
            "id": "2f939df3-631d-40cc-b665-fbc30a645ad3",
            "name": "admin01's Workspace",
            "status": "normal",
            "created_at": 1713058207
        }
    }
    '''
    def get_tenant(self, workspace_id):
        response = requests.get(self.DIFY_API_URL + "/console/api/all-workspaces/"+workspace_id, headers=self.admin_request_headers)
        response.raise_for_status()
        result = response.json()
        if result['data']:
            return result['data']
        return None


    '''
    根据账号ID获取账号信息接口
    响应
    {
        "data": {
            "id": "2028d435-ce19-4b6f-88c0-a49e92e18927",
            "name": "admin01",
            "avatar": null,
            "email": "dk@fyi.ac.cn",
            "is_password_set": true,
            "interface_language": "en-US",
            "interface_theme": "light",
            "timezone": "America/New_York",
            "last_login_at": 1715503132,
            "last_login_ip": "127.0.0.1",
            "status": "active",
            "created_at": 1713058194
        }
    }
    '''
    def get_account(self, account_id):
        response = requests.get(self.DIFY_API_URL + "/console/api/accounts/"+account_id, headers=self.admin_request_headers)
        response.raise_for_status()
        result = response.json()
        if result['data']:
            return result['data']
        return None


    '''
    激活用户接口
    响应
    {
        "result": "success"
    }
    '''
    def account_update_status(self, account_id, status):
        json_data = {
            "status": status
        }
        response = requests.put(self.DIFY_API_URL + "/console/api/accounts/"+account_id+"/update-status", json=json_data, headers=self.admin_request_headers)
        response.raise_for_status()
        result = response.json()
        if result['result']:
            return result['result']
        return 'fail'


    '''
    微信与账号绑定接口
    响应
    {
        "data": {
            "result": true
        }
    }
    '''
    def link_account_integrate(self, provider, open_id, account_id):
        json_data = {
            "account_id": account_id,
            "provider": provider,
            "open_id": open_id
        }
        logging.info(json_data)
        response = requests.post(self.DIFY_API_URL + "/console/api/account-integrates", json=json_data, headers=self.admin_request_headers)
        logging.info(response)
        response.raise_for_status()
        result = response.json()
        if result['data']:
            return result['data']['result']
        return True


    '''
    创建账号信息接口
    响应
    {
        "data": {
            "id": "4dd56fbc-7d30-4b93-b95c-975b7daf96d9",
            "name": "account-name",
            "avatar": null,
            "email": "new-new-email@racio.chat",
            "is_password_set": false,
            "interface_language": "en-US",
            "interface_theme": "light",
            "timezone": "America/New_York",
            "last_login_at": null,
            "last_login_ip": null,
            "status": "pending",
            "created_at": 1715684052
        }
    }
    '''
    def create_account(self, name, email):
        json_data = {
            "name": name,
            "email": email
        }
        response = requests.post(self.DIFY_API_URL + "/console/api/accounts", json=json_data, headers=self.admin_request_headers)
        response.raise_for_status()
        if response.status_code == 201:
            result = response.json()
            if result['data']:
                return result['data']
        return None


    '''
    查询email是否已存在
    响应
    {
        "data": {
            "email": "dk@fyi.ac.cn",
            "result": true
        }
    }
    '''
    # def verify_email(self, email):
    #     params = {
    #         'email': email
    #     }
    #     response = requests.get(self.DIFY_API_URL + "/console/api/accounts/verify-email", params=params, headers=self.admin_request_headers)
    #     response.raise_for_status()
    #     result = response.json()
    #     if result['data']:
    #         return result['data']['result']
    #     return True


    '''
    获取owner空间信息接口
    响应
    {
        "data": [
            "786923ae-b8d4-43b6-baeb-bbd64099d75d",
            "786923ae-b8d4-43b6-baeb-bbd64099d75e"
        ]
    }
    '''
    # def get_tenant_id(self, account_id, role):
    #     params = {
    #         'account_id': account_id,
    #         'role': role
    #     }
    #     response = requests.get(self.DIFY_API_URL + "/console/api/all-workspaces/match-account", params=params, headers=self.admin_request_headers)
    #     response.raise_for_status()
    #     result = response.json()
    #     if result['data']:
    #         return result['data']
    #     return None


    '''
    加入空间接口
    响应
    {
        "tenant_id": "786923ae-b8d4-43b6-baeb-bbd64099d7ff",
        "account_id": "54ada6af-6620-42d0-91bc-73cfb6c062db",
        "role": "owner"
    }
    '''
    def create_tenant_member(self, tenant_id, account_id, role):
        json_data = {
            'tenant_id': tenant_id,
            'account_id': account_id,
            'role': role
        }
        response = requests.post(self.DIFY_API_URL + "/console/api/all-workspaces/add-member", json=json_data, headers=self.admin_request_headers)
        response.raise_for_status()
        result = response.json()
        if result:
            return result
        return None


    '''
    创建空间接口
    响应
    {
        "data": {
            "id": "8f3e4eb2-65b8-4d90-b1a9-4ef7dbac4fa8",
            "name": "new name for worksapce",
            "status": "normal",
            "created_at": 1715758094
        }
    }
    '''
    def create_tenant(self, name, owner_email):
        json_data = {
            'name': name,
            'owner_email': owner_email,
        }
        response = requests.post(self.DIFY_API_URL + "/console/api/all-workspaces", json=json_data, headers=self.admin_request_headers)
        response.raise_for_status()
        if response.status_code == 201:
            result = response.json()
            if result['data']:
                return result['data']
        return None


    '''
    切换空间接口
    响应
    {
        "result":"success",
        "new_tenant": {
            'id': tenant.id,
            'name': tenant.name,
            'plan': tenant.plan,
            'status': tenant.status,
            'created_at': tenant.created_at,
            'in_trail': True,
            'trial_end_reason': None,
            'role': 'normal',
        }
    }
    '''
    def switch_tenant(self, tenant_id):
        json_data = {
            'tenant_id': tenant_id
        }
        response = requests.post(self.DIFY_API_URL + "/console/api/workspaces/switch", json=json_data, headers=self.user_request_headers)
        response.raise_for_status()
        result = response.json()
        if result['new_tenant']:
            return result['new_tenant']
        return None


    '''
    获取用户的加入的空间接口
    响应
    {
        "data": [
            {
                "id": "b9a20841-9128-4719-a81a-d449ed37c2ca",
                "name": "account-name's Workspace",
                "plan": "basic",
                "status": "normal",
                "role":"",
                "created_at": 1715684052,
                "current": null
            },
            {
                "id": "8f3e4eb2-65b8-4d90-b1a9-4ef7dbac4fa8",
                "name": "new name for worksapce",
                "plan": "basic",
                "status": "normal",
                "role":"",
                "created_at": 1715758094,
                "current": null
            }
        ]
    }
    '''
    def get_all_tenant(self, account_id):
        params = {
            "account_id": account_id
        }
        response = requests.get(self.DIFY_API_URL + "/console/api/all-workspaces/get-tenants", params=params, headers=self.admin_request_headers)
        response.raise_for_status()
        result = response.json()
        if result['data']:
            return result['data']
        return None


    '''
    将用户移出当前空间接口
    响应
    {
        "result":"success",
    }
    '''
    def member_cancel_invite(self, account_id):
        response = requests.delete(self.DIFY_API_URL + "/console/api/workspaces/current/members/"+account_id, headers=self.user_request_headers)
        response.raise_for_status()
        result = response.json()
        if result['result']:
            return result['result']
        return None


    '''
    切换用户角色接口
    响应
    {
        "result":"success",
    }
    '''
    def member_update_role(self, account_id, role):
        data = {
            "role": role
        }
        response = requests.put(self.DIFY_API_URL + "/console/api/workspaces/current/members/" + account_id + "/update-role", data=data, headers=self.user_request_headers)
        response.raise_for_status()
        result = response.json()
        if result['result']:
            return result['result']
        return None


    '''
    根据空间ID，获取该空间里的所有账号接口
    响应
    {
        "data": [
            {
                "id": "2028d435-ce19-4b6f-88c0-a49e92e18927",
                "name": "admin01",
                "avatar": null,
                "email": "dk@fyi.ac.cn",
                "last_login_at": 1715503132,
                "created_at": 1713058194,
                "role": "normal",
                "status": "active"
            },
            {
                "id": "85e41d03-1d8d-4513-b8d1-e0358aab0aad",
                "name": "account-name",
                "avatar": null,
                "email": "new-new-email@racio.chat",
                "last_login_at": null,
                "created_at": 1715755368,
                "role": "owner",
                "status": "pending"
            }
        ]
    }
    '''
    def get_members(self):
        response = requests.get(self.DIFY_API_URL + "/console/api/workspaces/current/members", headers=self.user_request_headers)
        response.raise_for_status()
        result = response.json()
        if result['accounts']:
            return result['accounts']
        return None


    '''
    根据账号ID，角色获取该用户加入的空间
    响应
    {
        "data": [
            "786923ae-b8d4-43b6-baeb-bbd64099d75d",
            "786923ae-b8d4-43b6-baeb-bbd64099d75e"
        ]
    }
    '''
    def get_account_tenant_info(self, account_id, role):
        params = {
            "account_id": account_id,
            "role": role
        }
        response = requests.get(self.DIFY_API_URL + "/console/api/all-workspaces/match-account", params=params, headers=self.admin_request_headers)
        response.raise_for_status()
        result = response.json()
        if result['data']:
            return result['data']
        return None


