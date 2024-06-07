<template>
    <div class="login-container">
        checking...
    </div>

</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue"

import { getQueryObject } from "@/utils/index"
import { getGZHInfo, checkOpenId, getJwtToken } from "@/api/api"
import { ElMessage, ElMessageBox } from "element-plus"
import { useRouter } from "vue-router"
import { useUserStore } from "@/store/modules/user"
const router = useRouter()
const urlQuery = getQueryObject(null)
const accessToken = ref("")

const UserStore = useUserStore()
function GZHInfo() {

    getGZHInfo({ code: urlQuery.code })
        .then(res => {
            let { code, data, msg } = res.data
            if (code == 0) {
                accessToken.value = data
                check(data)
            }
        })
        .catch(err => {
            ElMessage({
                message: err.response.data.message,
                type: 'error',
            })
        })




}
function goTo(uri) {
    if (uri.indexOf("http") != -1) {
        location.href = uri
    } else {
        router.push(uri)
    }
}
function check(access_token) {

    checkOpenId({ "access_token": access_token })
        .then(res => {
            let { code, data, msg } = res.data
            console.log(code, data, "status, data");

            if (code == 0 && data == true) {
                getJwtToken({ "access_token": access_token })
                    .then(res => {
                        let { code, data, msg } = res.data
                        if (code == 0) {
                            let userInfo = {
                                token: data.token,
                                access_token: access_token,
                                roles: [data.account_role],
                                username: data.account_role == "owner" ? "空间所有者" : data.account_role == "admin" ? "空间管理员" : "尊享会员",
                            }
                            UserStore.login(userInfo)
                            const uri = import.meta.env.VITE_APP_DIFY_URL ? import.meta.env.VITE_APP_DIFY_URL : window.globalVariable.DIFY_URL
                            window.location.href = `${uri}?console_token=${data.token}`
                        }
                    })


            } else {

                ElMessageBox.alert('该微信未被绑定，请联系管理员', '提示', {
                    confirmButtonText: '知道了',
                    callback: () => {
                        router.back()
                    },
                })
            }
        })




}
onMounted(() => {

    GZHInfo()
})
</script>
<style lang="scss" scoped>
@import "./index";
</style>
