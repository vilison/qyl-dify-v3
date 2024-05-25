import json
from flask import Flask
from libs.tencentcloud.common import credential
from libs.tencentcloud.common.profile.client_profile import ClientProfile
from libs.tencentcloud.common.profile.http_profile import HttpProfile
from libs.tencentcloud.sms.v20210111 import sms_client, models


class Sms:
    def __init__(self):
        self._client = None
        self.smsSdkAppId = ''
        self.templateId = ''
        self.signName = ''
        self.timeOut = '5'

    def is_inited(self) -> bool:
        return self._client is not None

    def init_app(self, app: Flask):
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        cred = credential.Credential(app.config.get('TENCENT_SECRET_ID'), app.config.get('TENCENT_SECRET_KEY'))
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "sms.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        self._client = sms_client.SmsClient(cred, "ap-guangzhou", clientProfile)
        self.smsSdkAppId = app.config.get('TENCENT_SMS_SDK_APP_ID')
        self.templateId = app.config.get('TENCENT_SMS_TEMPLATE_ID')
        self.signName = app.config.get('TENCENT_SMS_SIGNNAME')
        self.timeOut = app.config.get('TENCENT_SMS_TIMEOUT')

    def send(self, phone: str, code: str):
        if not self._client:
            raise ValueError('Sms client is not initialized')

        if not phone:
            raise ValueError('sms phone is not set')

        if not code:
            raise ValueError('sms code is not set')

        req = models.SendSmsRequest()
        params = {
            "PhoneNumberSet": [phone],
            "SmsSdkAppId": self.smsSdkAppId,
            "TemplateId": self.templateId,
            "TemplateParamSet": [code, self.timeOut],
            "SignName": self.signName
        }
        # print(params)
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个SendSmsResponse的实例，与请求对象对应
        resp = self._client.SendSms(req)
        # 输出json格式的字符串回包
        print(resp.to_json_string())


def init_app(app: Flask):
    sms.init_app(app)


sms = Sms()
