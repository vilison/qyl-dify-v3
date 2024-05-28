<template>
    <div class="login-qrcode">
        <h2 class="title">Racio用户登录</h2>
        <div id="snsapi_login"></div>

        <wxlogin appid="wx14d04b12be5b6bb1" scope="snsapi_login" :redirect_uri="encodeURIComponent(redirect_uri)">
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
})
const redirect_uri = `${import.meta.env.VITE_APP_WEBSITE}/#/auth/check?token=${props.token}`
</script>

<style lang="scss" scoped>
@import "../index";
</style>
