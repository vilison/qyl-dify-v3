<template>
    <div class="login-qrcode">

        <div id="snsapi_login"></div>
        <wxlogin :appid="appid" :state="props.source" scope="snsapi_login"
            :redirect_uri="encodeURIComponent(redirect_uri)"
            :href="'data:text/css;base64,LmltcG93ZXJCb3ggLnRpdGxlIHsKIGRpc3BsYXk6IG5vbmU7Cn0KLmltcG93ZXJCb3ggLnN0YXR1cy5zdGF0dXNfYnJvd3NlciB7CiBkaXNwbGF5OiBub25lOwp9Ci5pbXBvd2VyQm94IC5xcmNvZGUgewogYm9yZGVyOiBub25lOwogd2lkdGg6IDIwMHB4OwogaGVpZ2h0OiAyMDBweDsKfQouaW1wb3dlckJveCAuc3RhdHVzewogZGlzcGxheTogbm9uZQp9'">
        </wxlogin>
        <div class="qrcode-text">请使用微信扫描二维码登录</div>
        <div class="agreement-tips">扫码即同意<a href="https://www.racio.chat/privacy" target="_blank">隐私政策</a>”和“<a
                href="https://www.racio.chat/terms" target="_blank">服务条款</a>”</div>
    </div>
</template>

<script lang="ts" setup>
import { onMounted } from "vue"
import wxlogin from "vue-next-wxlogin"
let props = defineProps({
    token: {
        type: String,
        default: "",
    },
    source: {
        type: String,
        default: "index",
    }
})
const uri = import.meta.env.VITE_APP_WEBSITE ? import.meta.env.VITE_APP_WEBSITE : window.globalVariable.WEBSITE
const appid = import.meta.env.VITE_APP_APPID ? import.meta.env.VITE_APP_APPID : window.globalVariable.APPID
const redirect_uri = `${uri}/auth/check?token=${props.token}`

</script>

<style lang="scss" scoped>
@import "../index";

.login-qrcode {
    height: 270px;
}

.qrcode-text {
    font-size: 14px;
    font-weight: 600;
}
</style>
