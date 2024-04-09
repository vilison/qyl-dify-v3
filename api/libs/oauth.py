import urllib.parse
from dataclasses import dataclass

import requests


@dataclass
class OAuthUserInfo:
    id: str
    name: str
    email: str


class OAuth:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorization_url(self):
        raise NotImplementedError()

    def get_access_token(self, code: str):
        raise NotImplementedError()

    def get_raw_user_info(self, token: str):
        raise NotImplementedError()

    def get_user_info(self, token: str) -> OAuthUserInfo:
        raw_info = self.get_raw_user_info(token)
        return self._transform_user_info(raw_info)

    def _transform_user_info(self, raw_info: dict) -> OAuthUserInfo:
        raise NotImplementedError()


# racio.chat/console/api/oauth/authorize/wechat
#
# 在微信用户授权登录已接入微信OAuth2.0的第三方应用后，第三方可以获取到用户的接口调用凭证（access_token），
# 通过access_token可以进行微信开放平台授权关系接口调用，从而可实现获取微信用户基本开放信息和帮助用户实现基础开放功能等。
# 微信OAuth2.0授权登录目前支持authorization_code模式，适用于拥有server端的应用授权。该模式整体流程为：
# 1. 第三方发起微信授权登录请求，微信用户允许授权第三方应用后，微信会拉起应用或重定向到第三方网站，并且带上授权临时票据code参数；
# 2. 通过code参数加上AppID和AppSecret等，通过API换取access_token；
# 3. 通过access_token进行接口调用，获取用户基本数据资源或帮助用户实现基本操作。
#
class WeChatOAuth(OAuth):
    _AUTH_URL = 'https://open.weixin.qq.com/connect/qrconnect'
    # snsapi_base 通过code换取access_token、refresh_token和已授权scope
    _TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    # snsapi_userinfo 获取用户个人信息
    _USER_INFO_URL = 'https://api.weixin.qq.com/sns/userinfo'

    _EMAIL_INFO_URL = 'https://api.github.com/user/emails'
    
    _OPEN_ID = ''

    def get_authorization_url(self):
        params = {
            'appid': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',    # code
            'scope': 'snsapi_login',    # Request only for web app,
            'state': 'cZMf3Qha10NP4NkhSkqoAMldbeifDhKqRzSbmmVYfuctHEYQxS4GfkIf'  # random/session to avoid csrf attack
        }
        return f"{self._AUTH_URL}?{urllib.parse.urlencode(params)}#wechat_redirect"

    # get access_token via code
    def get_access_token(self, code: str):
        # request: GET
        # https://api.weixin.qq.com/sns/oauth2/access_token?
        #   appid=APPID&
        #   secret=SECRET&
        #   code=CODE&
        #   grant_type=authorization_code
        #
        # return:
        #     {
        #         "access_token": "ACCESS_TOKEN",
        #         "expires_in": 7200,
        #         "refresh_token": "REFRESH_TOKEN",
        #         "openid": "OPENID",
        #         "scope": "SCOPE",
        #         "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
        #     }
        # or 
        #     { "errcode":40029, "errmsg":"invalid code" }
        params = {
            'appid': self.client_id,        # AppId
            'secret': self.client_secret,   # AppSecret
            'code': code,
            'grant_type': 'authorization_code' # authorization_code
        }
        headers = {'Accept': 'application/json'}
        response = requests.get(url=f'{self._TOKEN_URL}?{urllib.parse.urlencode(params)}', headers=headers)
        response_json = response.json()
        access_token = response_json.get('access_token')
        openid = response_json.get('openid')

        if not access_token:
            raise ValueError(f"Error in WeChat OAuth: {response_json}")
        if not openid:
            raise ValueError(f"Error in WeChat OAuth: {response_json}")

        self._OPEN_ID = openid
        return access_token

    def get_raw_user_info(self, token: str):
        # request: GET
        # https://api.weixin.qq.com/sns/userinfo?
        #   access_token=ACCESS_TOKEN&
        #   openid=OPENID
        
        # return: 
        # {
        #     "openid":"OPENID",        # 普通用户的标识，对当前开发者账号唯一
        #     "nickname":"NICKNAME",
        #     "sex":1,
        #     "province":"PROVINCE",
        #     "city":"CITY",
        #     "country":"COUNTRY",
        #     "headimgurl": "https://thirdwx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0",
        #     "privilege":[
        #         "PRIVILEGE1", # 用户特权信息，json数组，如微信沃卡用户为（chinaunicom）
        #         "PRIVILEGE2"
        #     ],
        #     "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL"   # 用户统一标识。针对一个微信开放平台账号下的应用，同一用户的unionid是唯一的。
        # }
        # or 
        #   { "errcode":40003, "errmsg":"invalid openid" }
        params = {
            'access_token': token,        
            'openid': self._OPEN_ID,          
        }
        headers = {'Accept': 'application/json'}
        response = requests.get(url=f'{self._USER_INFO_URL}?{urllib.parse.urlencode(params)}', headers=headers)
        # esponse.raise_for_status() returns an HTTPError object if an error has occurred during the process. 
        # It is used for debugging the requests module and is an integral part of Python requests.
        response.raise_for_status()
        user_info = response.json()

        return {**user_info}    # unpacking

    def _transform_user_info(self, raw_info: dict) -> OAuthUserInfo:
        return OAuthUserInfo(
            id=str(raw_info['unionid']),
            name=raw_info['nickname'],
            email=None
        )


class GitHubOAuth(OAuth):
    _AUTH_URL = 'https://github.com/login/oauth/authorize'
    _TOKEN_URL = 'https://github.com/login/oauth/access_token'
    _USER_INFO_URL = 'https://api.github.com/user'
    _EMAIL_INFO_URL = 'https://api.github.com/user/emails'

    def get_authorization_url(self):
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'user:email'  # Request only basic user information
        }
        return f"{self._AUTH_URL}?{urllib.parse.urlencode(params)}"

    def get_access_token(self, code: str):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        headers = {'Accept': 'application/json'}
        response = requests.post(self._TOKEN_URL, data=data, headers=headers)

        response_json = response.json()
        access_token = response_json.get('access_token')

        if not access_token:
            raise ValueError(f"Error in GitHub OAuth: {response_json}")

        return access_token

    def get_raw_user_info(self, token: str):
        headers = {'Authorization': f"token {token}"}
        response = requests.get(self._USER_INFO_URL, headers=headers)
        response.raise_for_status()
        user_info = response.json()

        email_response = requests.get(self._EMAIL_INFO_URL, headers=headers)
        email_info = email_response.json()
        primary_email = next((email for email in email_info if email['primary'] == True), None)

        return {**user_info, 'email': primary_email['email']}

    def _transform_user_info(self, raw_info: dict) -> OAuthUserInfo:
        email = raw_info.get('email')
        if not email:
            email = f"{raw_info['id']}+{raw_info['login']}@users.noreply.github.com"
        return OAuthUserInfo(
            id=str(raw_info['id']),
            name=raw_info['name'],
            email=email
        )


class GoogleOAuth(OAuth):
    _AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
    _TOKEN_URL = 'https://oauth2.googleapis.com/token'
    _USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'

    def get_authorization_url(self):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': 'openid email'
        }
        return f"{self._AUTH_URL}?{urllib.parse.urlencode(params)}"

    def get_access_token(self, code: str):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }
        headers = {'Accept': 'application/json'}
        response = requests.post(self._TOKEN_URL, data=data, headers=headers)

        response_json = response.json()
        access_token = response_json.get('access_token')

        if not access_token:
            raise ValueError(f"Error in Google OAuth: {response_json}")

        return access_token

    def get_raw_user_info(self, token: str):
        headers = {'Authorization': f"Bearer {token}"}
        response = requests.get(self._USER_INFO_URL, headers=headers)
        response.raise_for_status()
        return response.json()

    def _transform_user_info(self, raw_info: dict) -> OAuthUserInfo:
        return OAuthUserInfo(
            id=str(raw_info['sub']),
            name=None,
            email=raw_info['email']
        )


