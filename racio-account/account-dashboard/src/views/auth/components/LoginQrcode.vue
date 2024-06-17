<template>
    <div class="login-qrcode">
        <h2 class="title">Racio用户登录</h2>
        <div id="snsapi_login"></div>

        <wxlogin :appid="appid" :state="props.source" scope="snsapi_login"
            :redirect_uri="encodeURIComponent(redirect_uri)">
        </wxlogin>
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
</style>
