<template>

    <div style="margin-right:20px;font-weight: 600;" v-if="!user.roles.includes('superAdmin')">
        当前空间:{{ UserStore.workspace_name }}
    </div>
    <el-button type="primary" @click="show" style="margin-right:20px"
        v-if="!user.roles.includes('superAdmin') && TenantList.length > 1">
        切换空间
    </el-button>


    <el-dialog v-model="dialogVisible" title="关联的工作空间" width="40%">
        <el-row :gutter="20">

            <el-col :span="8" style="margin-bottom:10px" v-for="(item, index) in TenantList">
                <div style="width: 100%">
                    <el-card shadow="always" @click="swtichTenant(item.id)" style="cursor: pointer;">
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
    </el-dialog>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue"
import { ElMessage } from "element-plus"
import { accountTenantList, tenantSwitch, getJwtToken } from "@/api/api"
import router from "@/routers";
const dialogVisible = ref(false)
const TenantList = ref([])
import { useUserStore } from "@/store/modules/user"
const user = useUserStore()
const workspace = ref({
    name: "",
    id: "",
})

const UserStore = useUserStore()
const show = () => {
    dialogVisible.value = true
}


function swtichTenant(tenant_id) {
    let data = {
        tenant_id: tenant_id
    }
    tenantSwitch(data)
        .then(res => {
            let { code, data, msg } = res.data
            if (code == 0) {
                localStorage.setItem("tenant_id", data.tenant_id)
                localStorage.setItem("workspace_name", data.name)
                localStorage.setItem("roles", `["${data.role}"]`)

                UserStore.roles = [data.role] // data.role
                UserStore.workspace_name = data.name

                dialogVisible.value = false

                location.reload()
            }
        })
}

defineExpose({
    show,
})


function JwtToken() {
    getJwtToken({ "access_token": localStorage.access_token })
        .then(res => {
            let { code, data, msg } = res.data
            if (code == 0) {
                workspace.value.name = data.tenant_name
                workspace.value.id = data.tenant_id
                UserStore.tenantId = data.tenant_id
                localStorage.setItem("tenant_id", data.tenant_id)

            }
        })
}
onMounted(() => {
    JwtToken()
    accountTenantList()
        .then(res => {
            let { code, data, msg } = res.data
            if (code == 0) {
                TenantList.value = data
            } else {
                user.logout()
            }

        })
})
</script>
