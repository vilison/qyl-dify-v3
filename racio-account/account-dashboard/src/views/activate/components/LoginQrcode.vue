<template>
    <div class="login-qrcode">
        <h2 class="title">
            <h4>邀请您体验{{ role == "owner" ? "新" : workspace_name }}的AI数字员工{{ role == "owner" ? "所有者 " : role ==
                "admin" ? "管理员 " : "使用者 " }}</h4>
            <h5>请用您的微信扫码登录，方便后续使用</h5>
        </h2>
        <div id="snsapi_login"></div>
        <wxlogin appid="wx14d04b12be5b6bb1" scope="snsapi_login" :redirect_uri="encodeURIComponent(redirect_uri)">
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


const redirect_uri = `${import.meta.env.VITE_APP_WEBSITE}/#/activate/phone?token=${props.token}`


onMounted(() => {
    console.log(redirect_uri, "redirect_uri");
})




</script>

<style lang="scss" scoped>
@import "../index";

.login-box .login-form {
    padding: 12px
}

.title {
    text-align: center;
}
</style>
