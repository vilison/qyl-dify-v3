<template>
    <div class="login-container">
        <div class="login-box">
            <SwitchDark class="login-dark" />

            <div class="login-form">

                <LoginForm />

            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import LoginForm from "./components/LoginForm.vue"
import SwitchDark from "@/components/SwitchDark/index.vue"
import { useRouter } from "vue-router"
import { useUserStore } from "@/store/modules/user"
const router = useRouter()
const { token, roles, isLogin } = useUserStore()

if (isLogin) {

    if (roles.some((item) => item == "superAdmin")) {
        router.replace({ path: "/admin" })
    } else if (roles.some((item) => item == "admin") || roles.some((item) => item == "owner")) {
        router.replace({ path: "/workspace" })
    }
}

</script>
<style lang="scss" scoped>
@import "./index";
</style>
