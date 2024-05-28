<template>
    <div class="login-container">
        <div class="login-box">
            <SwitchDark class="login-dark" />

            <div class="login-form">
                <LoginQrcode v-if="showQrcode" :token="token" :role="role" :workspace_name="workspace_name" />
                <div style="text-align: center;" v-else>
                    <h2>此邀请链接已经失效<br />请联系管理员（微信：dukexls）<br />获得新的邀请链接</h2>
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

const showQrcode = ref(false)
const role = ref("")
const workspace_name = ref("")
const { token, code } = getQueryObject(null)
function checkToekn() {

    checkInvitToken({ token: token })
        .then(res => {
            let { code, msg, data } = res.data
            if (code == 0) {

                if (data.is_valid) {
                    role.value = data.role
                    workspace_name.value = data.workspace_name
                    showQrcode.value = true

                }

            }
        })

}
onMounted(async () => {

    checkToekn()

})
</script>
<style lang="scss" scoped>
@import "./index";
</style>
