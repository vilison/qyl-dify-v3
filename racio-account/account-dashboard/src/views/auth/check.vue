<template>
    <div class="login-container">
        checking...
    </div>


    <el-dialog v-model="dialogSelectVisible" title="登录成功" :close-on-click-modal="false" :close-on-press-escape="false"
        :show-close="false">
        <el-row>
            <el-col :span="5">
                <el-card @click="goTo('/account')" style="cursor: pointer;">
                    进入管理后台
                </el-card>
            </el-col>
        </el-row>
        <el-row>
            <el-col>
                <h3>选择进入的工作空间</h3>
            </el-col>
            <el-col :span="5">
                <el-card>
                    进入管理后台
                </el-card>
            </el-col>
        </el-row>
    </el-dialog>

</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue"

import { getQueryObject } from "@/utils/index"
import { getWxInfo, checkOpenId, getJwtToken } from "@/api/api"
import { ElMessage, ElMessageBox } from "element-plus"
import { useRouter } from "vue-router"
import { useUserStore } from "@/store/modules/user"
const router = useRouter()
const urlQuery = getQueryObject(null)
const accessToken = ref("")
const dialogSelectVisible = ref(false)
const UserStore = useUserStore()
function WxInfo() {

    getWxInfo({ token: urlQuery.token, code: urlQuery.code })
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
                                roles: [data.account_role]
                            }
                            UserStore.login(userInfo)

                            window.location.href = `${import.meta.env.VITE_APP_DIFY_URL}?console_token=${data.token}`
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
    WxInfo()
})
</script>
<style lang="scss" scoped>
@import "./index";
</style>
