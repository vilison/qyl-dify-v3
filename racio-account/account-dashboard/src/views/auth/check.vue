<template>
    <div class="login-container">
        checking...
    </div>


    <el-dialog v-model="dialogSelectVisible" title="登录成功" :close-on-click-modal="false" :close-on-press-escape="false"
        :show-close="false">
        <el-row style="display:flex;align-items: center;justify-items: center;justify-content: center;">
            <el-col :span="12" style="display:flex;align-items: center;justify-items: center;justify-content: center;"
                v-if="currentRole != 'normal'">
                <el-button @click="goTo('/workspace')" style="cursor: pointer;">
                    进入管理后台
                </el-button>
            </el-col>
            <el-col :span="12" style="display:flex;align-items: center;justify-items: center;justify-content: center;">
                <el-button type="primary" @click="goTo(dify_url)">
                    进入Ai应用
                </el-button>
            </el-col>
        </el-row>
    </el-dialog>

</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue"

import { getQueryObject } from "@/utils/index"
import { getWxInfo, checkOpenId, getJwtToken, tenantSwitch } from "@/api/api"
import { ElMessage, ElMessageBox } from "element-plus"
import { useRouter } from "vue-router"
import { useUserStore } from "@/store/modules/user"
const router = useRouter()
const urlQuery = getQueryObject(null)
const accessToken = ref("")
const dialogSelectVisible = ref(false)
const UserStore = useUserStore()
const dify_url = ref("")
const currentRole = ref("normal")
function WxInfo() {

    getWxInfo({ code: urlQuery.code })
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
    console.log(uri, "localStorage.DIFY_TOKEN");

    if (uri.indexOf("http") != -1) {
        window.open(uri, '_blank')
    } else {
        router.replace(uri)
    }
}
function check(access_token) {
    checkOpenId({ "access_token": access_token })
        .then(res => {
            let { code, data, msg } = res.data

            if (code == 0 && data == true) {
                getJwtToken({ "access_token": access_token })
                    .then(res => {
                        let { code, data, msg } = res.data
                        if (code == 0) {

                            if (data.tenant_id == "" && data.current_role != "super_admin") {
                                ElMessageBox.alert('该Racio尚未找到您的关联帐号，请联系管理员（微信：dukexls）申请试用', '提示', {
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
                            swtichTenant(data.tenant_id)
                            currentRole.value = data.current_role
                            UserStore.login(userInfo)


                            dify_url.value = import.meta.env.VITE_APP_DIFY_URL ? `${import.meta.env.VITE_APP_DIFY_URL}?console_token=${data.token}` : `${window.globalVariable.DIFY_URL}?console_token=${data.token}`
                            localStorage.setItem("DIFY_TOKEN", data.token)

                            if (urlQuery.state == "index") {

                                location.href = dify_url.value
                            } else if (urlQuery.state == "auth") {
                                router.replace("/workspace")
                            } else {
                                dialogSelectVisible.value = true
                            }

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
    WxInfo()
})
</script>
<style lang="scss" scoped>
@import "./index";
</style>
