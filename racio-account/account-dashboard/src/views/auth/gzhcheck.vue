<template>
    <div class="login-container">
        checking...
    </div>

</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue"

import { getQueryObject } from "@/utils/index"
import { getGZHInfo, checkOpenId, getJwtToken, tenantSwitch } from "@/api/api"
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

                            if (data.tenant_id == "" && data.current_role != "super_admin") {
                                ElMessageBox.alert('Racio尚未找到您的关联帐号，请联系管理员（微信：dukexls）申请试用', '提示', {
                                    confirmButtonText: '知道了',
                                })
                                return
                            }
                            let userInfo = {
                                token: data.token,
                                access_token: access_token,
                                roles: [data.current_role],
                                workspace_name: data.tenant_name,
                                workspace_id: data.tenant_id,
                                username: data.name
                            }
                            UserStore.login(userInfo)
                            swtichTenant(data.tenant_id)
                            const uri = import.meta.env.VITE_APP_DIFY_URL ? import.meta.env.VITE_APP_DIFY_URL : window.globalVariable.DIFY_URL
                            window.location.href = `${uri}?console_token=${data.token}`
                        }
                    })


            } else {

                ElMessageBox.alert('Racio尚未找到您的关联帐号，请联系管理员（微信：dukexls）申请试用', '提示', {
                    confirmButtonText: '知道了',
                    callback: () => {
                        router.back()
                    },
                })
            }
        })




}

function swtichTenant(tenant_id) {
    let data = {
        tenant_id: tenant_id
    }
    tenantSwitch(data)
        .then(res => {
            let { code, data, msg } = res.data

        })
}

onMounted(() => {

    GZHInfo()
})
</script>
<style lang="scss" scoped>
@import "./index";
</style>
