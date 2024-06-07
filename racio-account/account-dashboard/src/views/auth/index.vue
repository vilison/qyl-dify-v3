<template>
    <div class="login-container">
        <div class="login-box">
            <SwitchDark class="login-dark" />

            <div class="login-form">
                <LoginQrcode :token="tokens" v-if="platform == 'pc'" />
                <div style="text-align: center;" v-else>
                    <el-button type="success" @click="GotoGZH">微信公众号授权登录</el-button>
                </div>
                <Footer />
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref } from "vue"

import SwitchDark from "@/components/SwitchDark/index.vue"
import LoginQrcode from "./components/LoginQrcode.vue"
import Footer from "@/components/Footer/index.vue"
import { getQueryObject } from "@/utils/index"
import { useUserStore } from "@/store/modules/user"
import { useRouter } from "vue-router"
import { onMounted } from "vue"
const router = useRouter()
const platform = ref("")


const { tokens } = ref(getQueryObject(null))



const { token, roles, isLogin } = useUserStore()

function isPlatform() {
    var ua = navigator.userAgent.toLowerCase();
    if (ua.match(/MicroMessenger/i) == "micromessenger") {
        platform.value = "wechat"
    } else {
        platform.value = "pc"
    }
}


function GotoGZH() {
    const appid = import.meta.env.VITE_APP_GZHAPPID ? import.meta.env.VITE_APP_GZHAPPID : window.globalVariable.GZHAPPID
    const redirect_uri = encodeURIComponent("http://at-stg.racio.chat/dashboard/auth/gzhcheck")
    // const redirect_uri = encodeURIComponent(import.meta.env.VITE_APP_WEBSITE ? import.meta.env.VITE_APP_WEBSITE : window.globalVariable.WEBSITE)
    const uri = `https://open.weixin.qq.com/connect/oauth2/authorize?appid=${appid}&redirect_uri=${redirect_uri}&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect`

    location.href = uri
}
onMounted(() => {
    isPlatform() // 判断平台


    if (isLogin) {

        if (roles.some((item) => item == "superAdmin")) {
            router.replace({ path: "/admin" })
        } else if (roles.some((item) => item == "admin") || roles.some((item) => item == "owner")) {
            router.replace({ path: "/account" })
        }
    }
})





</script>
<style lang="scss" scoped>
@import "./index";
</style>
