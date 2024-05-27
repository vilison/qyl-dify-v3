<template>
    <div style="margin-right:20px;font-weight: 600;">
        当前空间:{{ workspace_name }}
    </div>
    <el-button type="primary" @click="show" style="margin-right:20px">
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
import { accountTenantList, tenantSwitch } from "@/api/api"
import router from "@/routers";
const dialogVisible = ref(false)
const workspace_name = localStorage.getItem("workspace_name")
const TenantList = ref([])
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
                ElMessage.success("切换成功")
                dialogVisible.value = false
                location.reload()
            }
        })
}

defineExpose({
    show,
})
const tenantList = ref([])
onMounted(() => {
    accountTenantList()
        .then(res => {
            let { code, data, msg } = res.data
            TenantList.value = data

        })
})
</script>
