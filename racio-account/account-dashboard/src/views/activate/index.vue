<template>
    <div class="login-container">
        <div class="login-box">
            <SwitchDark class="login-dark" />

            <div class="login-form">
                <div>
                    <h2 class="title">
                        <span>邀请您体验{{ role == "owner" ? "新" : workspace_name }}的AI数字员工{{ role == "owner" ? "空间所有者" :
                            role
                                ==
                                "admin" ? "空间管理员" : "尊享会员" }}</span>

                    </h2>
                </div>
                <LoginQrcode v-if="platform == 'pc'" :token="token" :role="role" :workspace_name="workspace_name" />
                <div style="text-align: center;" v-else>
                    <h3>请通过授权微信公众号关联，方便后续使用</h3>
                    <el-button type="success" @click="GotoGZH">微信公众号授权关联</el-button>
                </div>
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
                    ElMessageBox.alert("<h2>此邀请链接已经失效<br />请联系管理员（微信：dukexls）<br />获得新的邀请链接</h2>", '提示', {
                        confirmButtonText: '知道了',
                        callback: () => {
                            router.back()
                        },
                    })
                }

            }
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
    const redirect_uri = encodeURIComponent(`${uri}/activate/phone?token=${token}`)
    const url = `https://open.weixin.qq.com/connect/oauth2/authorize?appid=${appid}&redirect_uri=${redirect_uri}&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect`

    location.href = url
}

onMounted(async () => {
    isPlatform()


})
</script>
<style lang="scss" scoped>
@import "./index";

.title {
    text-align: center;
    padding: 0;
    margin: 0;
}
</style>
