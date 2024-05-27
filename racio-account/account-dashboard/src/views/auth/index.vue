<template>
    <div class="login-container">
        <div class="login-box">
            <SwitchDark class="login-dark" />

            <div class="login-form">
                <LoginQrcode :token="tokens" />
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
const router = useRouter()



const { tokens } = ref(getQueryObject(null))



const { token, roles, isLogin } = useUserStore()

console.log(token, roles, isLogin, "token, roles, isLogin");


if (isLogin) {

    if (roles.some((item) => item == "superAdmin")) {
        router.replace({ path: "/admin" })
    } else if (roles.some((item) => item == "admin") || roles.some((item) => item == "owner")) {
        router.replace({ path: "/account" })
    }
}

</script>
<style lang="scss" scoped>
@import "./index";
</style>
