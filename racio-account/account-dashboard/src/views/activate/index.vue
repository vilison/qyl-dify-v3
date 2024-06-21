<template>
    <div class="login-container">
        <div class="login-box">
            <div class="login-text view_wechat">
                <h2 class="title">
                    <div>
                        <span>&#127881; 邀请您</span>
                        <div>作为【{{ role == "owner" ? "全新" : workspace_name }}】的</div>
                        <div>AI数字员工</div>
                        <div>办公空间的{{ role == "owner" ?
                            "所有者" : role == "admin" ? "管理员" : "尊享会员" }}</div>
                    </div>


                </h2>
            </div>
            <div class="login-form">
                <div class="view_pc">
                    <div class="login-text ">
                        <h2 class="title">
                            <div>
                                <span>&#127881; 邀请您</span>
                                <div>作为【{{ role == "owner" ? "全新" : workspace_name }}】的</div>
                                <div>AI数字员工</div>
                                <div>办公空间的{{ role == "owner" ?
                                    "所有者" : role == "admin" ? "管理员" : "尊享会员" }}</div>
                            </div>


                        </h2>
                    </div>
                </div>
                <LoginQrcode v-if="platform == 'pc'" :token="token" :role="role" :workspace_name="workspace_name" />
                <div style="text-align: center; margin:40px 0 100px;" v-else>

                    <el-button v-if="role == 'owner'" class="gzh-button" type="success"
                        @click="GotoGZH">立即进驻</el-button>
                    <el-button v-else class="gzh-button" type="success" @click="GotoGZH">微信授权登录</el-button>
                    <div class="agreement-tips">
                        授权即同意“<a href="https://www.racio.chat/privacy" target="_blank">隐私政策</a>”和“<a
                            href=" https://www.racio.chat/terms" target="_blank">服务协议</a>”
                    </div>
                </div>
            </div>
            <div class="login-footer">
                <Footer />
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue"

import SwitchDark from "@/components/SwitchDark/index.vue"
import LoginQrcode from "./components/LoginQrcode.vue"
import Footer from "@/components/Footer/index.vue"
import { getQueryObject } from "@/utils/index"
import { getWxInfo, checkInvitToken } from "@/api/api"
import { ElMessage, ElMessageBox } from "element-plus"
import { useRouter } from "vue-router"
const platform = ref("")
const showQrcode = ref(false)
const role = ref("")
const workspace_name = ref("")
const { token, code } = getQueryObject(null)
const router = useRouter()
function checkToekn() {

    checkInvitToken({ token: token })
        .then(res => {
            let { code, msg, data } = res.data
            if (code == 0) {

                if (data.is_valid) {
                    role.value = data.role
                    workspace_name.value = data.workspace_name
                    showQrcode.value = true

                } else {
                    ElMessageBox.alert(`此邀请链接已经失效，请联系${workspace_name.value == "" ? "管理员（微信：dukexls）" : workspace_name.value + '的[管理员]'}获得新的邀请链接`, '提示', {
                        confirmButtonText: '知道了',
                        dangerouslyUseHTMLString: true,
                        callback: () => {
                            router.back()
                        },
                    })
                }

            }
        })
        .catch(() => {
            ElMessageBox.alert(`此邀请链接已经失效，请联系${workspace_name.value == "" ? "管理员（微信：dukexls）" : workspace_name.value + '的[管理员]'}获得新的邀请链接`, '提示', {
                confirmButtonText: '知道了',
                dangerouslyUseHTMLString: true,
                callback: () => {
                    router.back()
                },
            })
        })

}
function isPlatform() {
    var ua = navigator.userAgent.toLowerCase();
    if (ua.match(/MicroMessenger/i) == "micromessenger") {
        platform.value = "wechat"
    } else {
        platform.value = "pc"
    }

    checkToekn()
}

function GotoGZH() {
    const uri = import.meta.env.VITE_APP_WEBSITE ? import.meta.env.VITE_APP_WEBSITE : window.globalVariable.WEBSITE
    const appid = import.meta.env.VITE_APP_GZHAPPID ? import.meta.env.VITE_APP_GZHAPPID : window.globalVariable.GZHAPPID
    const redirect_uri = encodeURIComponent(`${uri}/activate/gzhphone?token=${token}`)
    const url = `https://open.weixin.qq.com/connect/oauth2/authorize?appid=${appid}&redirect_uri=${redirect_uri}&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect`

    location.href = url
}

onMounted(async () => {
    isPlatform()


})
</script>
<style lang="scss" scoped>
@import "./index";

.agreement-tips {
    margin-top: 5px;
    font-size: 12px;
}
</style>
