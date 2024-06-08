<template>
    <div class="login-qrcode">
        <h2 class="title">
            <h5>请用您的微信扫码登录，方便后续使用</h5>
        </h2>
        <div id="snsapi_login"></div>
        <wxlogin :appid="appid" scope="snsapi_login" :redirect_uri="encodeURIComponent(redirect_uri)">
        </wxlogin>
    </div>
</template>

<script lang="ts" setup>
import { onMounted } from "vue"
import wxlogin from 'vue-next-wxlogin';
let props = defineProps({
    token: {
        type: String,
        default: "",
    },

    role: {
        type: String,
        default: "",
    },
    workspace_name: {
        type: String,
        default: "",
    },
})

const uri = import.meta.env.VITE_APP_WEBSITE ? import.meta.env.VITE_APP_WEBSITE : window.globalVariable.WEBSITE
const appid = import.meta.env.VITE_APP_APPID ? import.meta.env.VITE_APP_APPID : window.globalVariable.APPID
const redirect_uri = `${uri}/activate/phone?token=${props.token}`




</script>

<style lang="scss" scoped>
@import "../index";

.login-box .login-form {
    padding: 12px
}

.title {
    text-align: center;
    padding: 0;
    margin: 0;
}
</style>
