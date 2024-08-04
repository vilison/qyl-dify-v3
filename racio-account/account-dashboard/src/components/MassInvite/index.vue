<template>
    <el-button type="primary" :icon="CirclePlus" @click="openMassInvite">
        {{ roles.includes("superAdmin") ? "批量邀请开通工作空间" : "批量邀请成员" }}
    </el-button>


    <el-dialog v-model="inviteMassDialog" :title="roles.includes('superAdmin') ? '批量邀请开通工作空间' : '批量邀请成员'" width="500"
        align-center>
        <el-row>
            <el-col style="margin-bottom:20px">
                <span>输入被邀请人邮箱，如空则只生成邀请链接</span>
            </el-col>
        </el-row>
        <el-row v-if="roles.some(item => item !== 'superAdmin')" style="margin-bottom: 20px;">
            <el-select v-model="workspaceRole">
                <el-option v-for="item in rolesList" :key="item.key" :label="item.value" :value="item.key" />
            </el-select>
        </el-row>
        <el-row>
            <el-col style="margin-bottom:20px">
                <div>
                    <el-input v-model.number="invitMassQuota" style="width: 240px" placeholder="批量邀请数量 " clearable
                        :disabled="buttonMassStatus" />
                </div>

            </el-col>
        </el-row>
        <el-row>
            <el-col>
                <div>
                    <el-input v-model="remarkMassText" type="textarea" style="width: 240px" placeholder="备注 "
                        :disabled="buttonMassStatus" clearable />
                </div>

            </el-col>
        </el-row>
        <el-row>
            <el-col>
                <div v-if="invitMassUrl" style="border:#c9c9c9 2px dashed ; padding:5px;margin-top:5px"
                    @click="handleCopy(invitMassUrl, $event)">
                    点击复制邀请链接
                    <p>邀请链接：{{ invitMassUrl }}</p>
                </div>
            </el-col>
        </el-row>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="centerMassDialogVisible">取消</el-button>
                <el-button type="primary" @click="sendMassInvite" :disabled="buttonMassStatus">
                    发出邀请
                </el-button>
            </div>
        </template>
    </el-dialog>

</template>
<script lang="ts" setup>

import { ref, onMounted, defineEmits } from "vue"
import { ElMessage } from "element-plus"
import { CirclePlus } from '@element-plus/icons-vue'
import { inviteUser } from "@/api/api"
import { useUserStore } from "@/store/modules/user"
import clip from "@/utils/clipboard"
const invitMassQuota = ref(0)
const remarkMassText = ref("")
const invitMassUrl = ref("")
const inviteMassDialog = ref(false)
const buttonMassStatus = ref(false)
const { roles } = useUserStore()
const UserStore = useUserStore()
const workspaceRole = ref("")
const rolesList = ref([
    { key: "admin", value: "空间管理员" },
    { key: "normal", value: "尊享会员" }
])
const emit = defineEmits(['callFun'])

function centerMassDialogVisible() {
    invitMassQuota.value = 0
    inviteMassDialog.value = false
}

const handleCopy = (text, event) => {
    clip(text, event)
}
function openMassInvite() {
    inviteMassDialog.value = true
    buttonMassStatus.value = false
    invitMassUrl.value = ""
}


function sendMassInvite() {
    if (workspaceRole.value == "" && roles.includes("owner")) {
        ElMessage({
            message: "请选择邀请角色!",
            type: "error",
            duration: 3000,
        })
        return
    }
    if (invitMassQuota.value < 2) {
        ElMessage.error("批量邀请数量不能小于2")
        return
    }
    inviteUser({
        domain: "racio.chat",
        role: roles.includes("superAdmin") ? "owner" : workspaceRole.value,
        quota: invitMassQuota.value,
        tenant_id: UserStore.tenantId || localStorage.getItem("tenant_id"),
        remark: remarkMassText.value

    })
        .then(res => {
            let { code, data, msg } = res.data
            if (code == 0) {
                invitMassUrl.value = data.url
                buttonMassStatus.value = true
            }
        })
        .catch(error => {
            ElMessage({
                message: error.message,
                type: "error",
                duration: 3000,
            })
        })
        .finally(() => {
            emit('callFun')
        })
}

</script>
<style lang="scss" scoped>
.m-wangEditor {
    z-index: 99;
    width: 100%;
    border: 1px solid #cccccc;

    .editor-toolbar {
        border-bottom: 1px solid #cccccc;
    }

    .editor-content {
        overflow-y: hidden;
    }
}
</style>
