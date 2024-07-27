<template>
    <div class="login-container">
        <div class="login-box">
            <div class="login-text view-wechat">
                &#127881; 欢迎来到 <br /> Racio数字员工空间
            </div>


            <div class="login-form">
                <div class="login-text ">
                    <div class="view-pc">&#127881; 欢迎来到 <br /> Racio数字员工空间</div>
                </div>
                <LoginQrcode :token="tokens" :source="source" v-if="platform == 'pc'" />
                <div style="text-align: center;" v-else>
                    <el-button class="gzh-button" type="success" @click="GotoGZH">立即进入</el-button>
                    <div class="agreement-tips">授权即同意<a href="https://www.racio.chat/privacy"
                            target="_blank">隐私政策</a>”和“<a href="https://www.racio.chat/terms" target="_blank">服务条款</a>”
                    </div>
                </div>

            </div>
        </div>
        <div class="login-footer">
            <Footer />
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
const source = ref("index")

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
    const redirect_uri = encodeURIComponent(import.meta.env.VITE_APP_WEBSITE ? `${import.meta.env.VITE_APP_WEBSITE}/auth/gzhcheck` : `${window.globalVariable.WEBSITE}/auth/gzhcheck`)
    const uri = `https://open.weixin.qq.com/connect/oauth2/authorize?appid=${appid}&redirect_uri=${redirect_uri}&response_type=code&scope=snsapi_userinfo&state=index#wechat_redirect`

    location.href = uri
}
onMounted(() => {
    isPlatform() // 判断平台
    let us = localStorage.userState ? JSON.parse(localStorage.userState) : {}

    if (isLogin) {
        const uri = import.meta.env.VITE_APP_DIFY_URL ? import.meta.env.VITE_APP_DIFY_URL : window.globalVariable.DIFY_URL
        window.location.href = `${uri}?console_token=${us.token}`
    }




    // if (isLogin) {
    //     if (platform.value == "wechat") {
    //         const url = import.meta.env.VITE_APP_DIFY_URL ? `${import.meta.env.VITE_APP_DIFY_URL}` : `${window.globalVariable.DIFY_URL}`
    //         location.href = `${url}?console_token=${localStorage.token}`
    //     }
    //     else if (roles.some((item) => item == "superAdmin")) {
    //         router.replace({ path: "/admin" })
    //     } else if (roles.some((item) => item == "admin") || roles.some((item) => item == "owner")) {
    //         router.replace({ path: "/workspace" })
    //     }
    // }
})





</script>
<style lang="scss" scoped>
@import "./index";

.agreement-tips {
    margin-top: 5px;
    font-size: 12px;
    text-align: center;
}
</style>
<style>
#snsapi_login .impowerBox .loginPanel .title {
    display: none;
}
</style>