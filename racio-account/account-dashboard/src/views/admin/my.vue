<template>

    <div class="home-container">
        <el-row :gutter="20">

            <el-col :span="8" style="margin-bottom:10px" v-for="(item, index) in TenantList">
                <div style="width: 100%">
                    <el-card shadow="always" @click="openTenant(item.id)" style="cursor: pointer;">
                        <el-row>
                            <el-col>
                                <div style="font-weight: 600;font-size: 16px;">{{ item.name }} </div>
                            </el-col>
                            <el-col>
                                <div style="font-size: 12px;"><span style="font-size: 14px;">权限:</span>{{ item.role ==
                                    "owner" ? "空间所有者" :
                                    item.role == "admin" ? "管理员" :
                                        "普通用户" }} </div>
                            </el-col>
                            <el-col>
                                <div style="font-size: 12px;"><span style="font-size: 14px">空间状态：</span>{{ item.status
                                    == "normal" ? "正常使用" :
                                    "异常" }}
                                </div>
                            </el-col>
                        </el-row>

                    </el-card>
                </div>
            </el-col>

        </el-row>
    </div>

</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue"
import { Plus, Search } from '@element-plus/icons-vue'
import { ElMessage } from "element-plus"
import { useRouter } from "vue-router"
import { accountTenantList, tenantSwitch, getJwtToken } from "@/api/api"
import { useUserStore } from "@/store/modules/user"
import clip from "@/utils/clipboard"
import { formatTime } from "@/utils"

const UserStore = useUserStore()
const TenantList = ref([])

const searchTxt = ref("")
const router = useRouter()
const tableData = ref([])
const inviteDialog = ref(false)
const invitText = ref("")
const remarkText = ref("")
const invitUrl = ref("")
const PageInfo = ref({
    "page": 1,
    "limit": 10,
    "total": 0,
    "keyword": ""

})
const handleCopy = (text, event) => {
    clip(text, event)
}


function tenantList() {
    accountTenantList()
        .then(res => {
            let { code, data, msg } = res.data
            TenantList.value = data
        })
}
onMounted(() => {

    tenantList()
})


function openTenant(id) {
    let tenant = {
        "tenant_id": id
    }
    tenantSwitch(tenant)
        .then(res => {
            let { code, data, msg } = res.data
            if (code == 0) {
                localStorage.setItem("tenant_id", data.tenant_id)
                localStorage.setItem("workspace_name", data.tenant_name)
                let access_token = localStorage.getItem("access_token")

                getJwtToken({ "access_token": access_token })
                    .then(res => {
                        let { code, data, msg } = res.data
                        if (code == 0) {
                            let userInfo = {
                                token: data.token,
                                access_token: access_token,
                                roles: [data.account_role],
                                tenant_id: id
                            }
                            UserStore.login(userInfo)
                            const uri = import.meta.env.VITE_APP_DIFY_URL ? import.meta.env.VITE_APP_DIFY_URL : window.globalVariable.DIFY_URL
                            window.location.href = `${uri}?console_token=${data.token}`
                            swtichTenant(data.tenant_id)
                        }
                    })
            }
        })

}
</script>
<style lang="scss" scoped>
.home-container {
    width: 98%;
    margin: 32px;
}

@import "./index";
</style>
