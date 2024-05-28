<template>
    <div class="login-container">
        <div class="login-box">
            <div class="login-form">
                <el-row :gutter="5" style="padding-bottom: 10px;" v-if="invitTokenInfo.role == 'owner'">
                    <el-col>
                        <h3>创建空间</h3>
                    </el-col>
                    <el-col :span="18">
                        <el-tooltip :visible="checkWorkSpaceBtn.tips" class="box-item" effect="light"
                            :content="checkWorkSpaceBtn.tipstext ? checkWorkSpaceBtn.tipstext : '只能填写英文字母+数字组合8-30个字符'"
                            placement="top-end">
                            <el-input placeholder="请输入用户名/空间名" v-model.trim="workspace" minlength="8" maxlength="30"
                                clearable @input="isWorkspace" />
                        </el-tooltip>
                    </el-col>
                    <el-col :span="6">
                        <div class="check-code">
                            <el-button size="small" :loading="checkWorkSpaceBtn.loading" type="success"
                                @click="checkWorkSpace">
                                {{ checkWorkSpaceBtn.text }}
                            </el-button>

                        </div>
                    </el-col>
                </el-row>
                <el-row :gutter="5" style="padding-bottom: 10px;" v-if="showVerify">
                    <el-col>
                        <h3>绑定手机号</h3>
                    </el-col>
                    <el-col :span="18">
                        <div>
                            <el-input maxlength="11" clearable v-model.number="phoneNum" @input="isPhone"
                                placeholder="输入需要绑定的手机号码" />
                        </div>
                    </el-col>
                    <el-col :span="6">
                        <div class="check-code">
                            <el-button :loading="checkCodeBtn.loading" type="primary" @click="getCheckCode"> {{
                                checkCodeBtn.text }}
                            </el-button>
                        </div>
                    </el-col>
                </el-row>

                <el-row :gutter="20" :justify="'start'" style="padding-bottom: 10px;" v-if="showVerify">
                    <el-col :span="18">
                        <div>
                            <el-input maxlength="4" clearable v-model.number="verifyCode" placeholder="请输入验证码" />
                        </div>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="20" style="text-align:center">
                        <div>
                            <el-button size="large" :width="100" type="primary" @click="activateAccount">{{
                                invitTokenInfo.role == "owner" ? "关联并创建空间" : "关联工作空间"
                                }}</el-button>
                        </div>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col>

                    </el-col>
                </el-row>

            </div>
        </div>
        <Footer />
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue"
import Footer from "@/components/Footer/index.vue"
import { ElMessage, ElMessageBox } from "element-plus"
import { getWxInfo, sendSms, activate, checkOpenId, checkInvitToken } from "@/api/api"
import { getQueryObject } from "@/utils/index"
import { useRouter } from "vue-router"
import { useUserStore } from "@/store/modules/user"
const router = useRouter()
const phoneNum = ref("")
const phoneStatus = ref(false)
const verifyPhoneNum = ref("")
const verifyCode = ref("")
const openId = ref("")
const workspace = ref("")
const accessToken = ref("")
const showWorkspace = ref(false)
const showVerify = ref(false)
const UserStore = useUserStore()
const { token, code } = getQueryObject(null)
const invitTokenInfo = ref({
    is_valid: "",
    workspace_name: "",
    role: ""
})
function isPhone(value: string) {
    const reg = /^((13[0-9])|(14[5-7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$/
    if (reg.test(value)) {
        checkCodeBtn.value.disabled = false
        phoneStatus.value = true
    }
}
function isWorkspace() {
    const reg = /^[a-z0-9]{8,30}$/i

    if (!reg.test(workspace.value)) {
        checkWorkSpaceBtn.value.tips = true
    } else {
        checkWorkSpaceBtn.value.tips = false
    }
}

function WxInfo() {

    getWxInfo({ token: token, code: code })
        .then(res => {
            let { code, msg, data } = res.data
            if (code == 0) {
                accessToken.value = data
                localStorage.setItem("access_token", data)
                check(data)
            }

        })
        .catch(err => {
            ElMessage({
                message: "微信扫码异常，请重新扫码",
                type: 'error',
                duration: 5000,
            })
            setTimeout(() => {
                router.back()
            }, 5000);
        })


}

function checkToekn() {

    checkInvitToken({ token: token })
        .then(res => {
            let { code, msg, data } = res.data
            if (code == 0) {

                if (data.is_valid) {

                    invitTokenInfo.value = data

                    WxInfo()
                } else {

                    ElMessage({
                        message: '邀请链接已失效，请联系管理员（微信：dukexls）',
                        type: 'warning',
                        duration: 3000,
                    })
                }

            }
        })

}
function check(access_token) {
    checkOpenId({
        "access_token": access_token,
    })
        .then(res => {
            let { code, msg, data } = res.data
            if (code == 0) {
                if (data) {
                    activateAccount()
                } else {
                    showVerify.value = true
                }
            }

        })
}

function activateAccount() {
    if (accessToken.value == "") {
        ElMessage({
            message: '请先完成微信授权',
            type: 'warning',
        })
        router.back()
        return
    } else if (token == "") {
        ElMessage({
            message: '请先获取邀请链接，请联系管理员（微信：dukexls）获得新的邀请链接',
            type: 'warning',
        })
        return
    }
    activate({
        "token": token,
        "phone": `${verifyPhoneNum.value}`,
        "code": `${verifyCode.value}`,
        "access_token": accessToken.value,
        "tenant_name": workspace.value, //长度30个字符
    })
        .then(res => {
            let { code, msg, data } = res.data
            if (code == 0) {
                let userInfo = {
                    token: data.token,
                    roles: [data.account_role]
                }
                UserStore.login(userInfo)
                ElMessage({
                    message: '绑定成功',
                    type: 'success',
                })
                setTimeout(() => {
                    router.replace({
                        path: "/invitSuccess",
                    })
                }, 800);
            } else {
                ElMessage({
                    message: msg,
                    type: 'error',
                })
            }
        })
}
function sendmsm() {
    sendSms({ token: token, phone: phoneNum.value })
        .then(res => {
            let { code, msg, data } = res.data
            if (code == 0) {
                verifyPhoneNum.value = phoneNum.value
                ElMessage({
                    message: '验证码发送成功',
                    type: 'success',
                })

            } else {
                ElMessage({
                    message: msg,
                    type: 'error',
                })
            }
        })

}
function checkWorkSpace() {
    if (workspace.value == "") {
        checkWorkSpaceBtn.value.tips = true
    }

}
let checkWorkSpaceBtn = ref({
    text: '检查是否可用',
    loading: false,
    tips: false,
    duration: 60,
    tipstext: ""
})
let checkCodeBtn = ref({
    text: '获取验证码',
    loading: false,
    disabled: true,
    duration: 60,
    timer: null
})


const getCheckCode = () => {
    if (!phoneStatus.value) {
        ElMessage({
            message: '请输入手机号',
            type: 'warning',
        })
        return
    }
    // 倒计时期间按钮不能单击
    if (checkCodeBtn.value.duration !== 60) {
        checkCodeBtn.value.disabled = true

    } else {
        sendmsm() //调用发送短信接口
    }
    // 清除掉定时器
    checkCodeBtn.value.timer && clearInterval(checkCodeBtn.value.timer)
    // 开启定时器
    checkCodeBtn.value.timer = setInterval(() => {
        const tmp = checkCodeBtn.value.duration--
        checkCodeBtn.value.text = `${tmp}秒`
        if (tmp <= 0) {
            // 清除掉定时器
            clearInterval(checkCodeBtn.value.timer)
            checkCodeBtn.value.duration = 60
            checkCodeBtn.value.text = '重新获取'
            // 设置按钮可以单击
            checkCodeBtn.value.disabled = false
        }
    }, 1000)
}

onMounted(() => {
    checkToekn()

})

</script>
<style lang="scss" scoped>
.check-code {
    line-height: 42px;
    font-size: 12px;
    cursor: pointer
}

@import "./index";

.login-box {
    height: 80%
}

.login-container {
    display: block;
}
</style>
