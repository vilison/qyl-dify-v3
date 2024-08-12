<template>

    <div class="home-container">
        <el-row :gutter="20">
            <!-- <el-col :span="10">
                <div>
                    <el-input v-model="PageInfo.keyword" class="w-50 m-2" size="large" clearable placeholder="搜索手机号"
                        :prefix-icon="Search" />
                </div>
            </el-col>
            <el-col :span="2">
                <div style="padding-top: 4px;">
                    <el-buttoauthList">搜索</el-button>
                </div>
            </el-col> -->
            <el-col :span="10">
                <div style="padding-top: 4px;">
                    <el-button type="primary" :icon="Plus" @click="openInvite">
                        邀请开通工作空间
                    </el-button>
                    <MassInvite @callFun="authList" />
                </div>
            </el-col>
        </el-row>
        <el-row class="row-bg" :gutter="11">

            <el-col :span="24">
                <el-table :data="tableData" style="width: 100%">

                    <el-table-column prop="name" label="用户名" min-width="100" />
                    <el-table-column prop="nickname" label="昵称" min-width="100" />
                    <el-table-column prop="headimgurl" label="头像" width="80">
                        <template #default="scope">
                            <div>
                                <el-image :src="scope.row.headimgurl" style="width: 80%; height: 80%">
                                    <div slot="error" class="image-slot">
                                        <span>无头像</span>
                                    </div>
                                </el-image>
                            </div>
                        </template>
                    </el-table-column>

                    <el-table-column prop="phone" label="手机号码" width="120" />

                    <el-table-column prop="status" label="邀请状态" width="100">
                        <template #default="scope">
                            <div>{{ scope.row.status == "active" ? "正常" : "异常" }}</div>
                        </template>
                    </el-table-column>
                    <el-table-column prop="last_login_at" label="最后登录时间" width="150">
                        <template #default="scope">
                            <div>{{ scope.row.last_login_at == null ? "无登录" :
                                formatTime(scope.row.last_login_at,
                                    "") }}
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column prop="tenant_names" label="所在的空间" width="150">
                        <template #default="scope">
                            <el-dropdown v-if="scope.row.tenant_names.length > 1">
                                <span class="el-dropdown-link">
                                    多于1个空间
                                    <el-icon class="el-icon--right">
                                        <arrow-down />
                                    </el-icon>
                                </span>
                                <template #dropdown>
                                    <el-dropdown-menu>
                                        <el-dropdown-item v-for="item in scope.row.tenant_names">{{ item
                                            }}</el-dropdown-item>
                                    </el-dropdown-menu>
                                </template>
                            </el-dropdown>
                        </template>
                    </el-table-column>

                    <el-table-column prop="created_at" label="邀请时间" width="150">
                        <template #default="scope">
                            <div>{{ formatTime(scope.row.created_at, "") }}</div>
                        </template>
                    </el-table-column>
                    <el-table-column prop="email" label="邮箱" width="180" />
                    <el-table-column prop="id" label="用户ID" width="290" />
                    <!-- <el-table-column label="操作" fixed="right" width="200">
                        <template #default="scope">
                            <el-button type="primary" @click="editRolesDialog(scope.row)">修改权限</el-button>
                            <el-button type="danger" @click="deleteDialog(scope.row)">移除</el-button>
                        </template>
                    </el-table-column> -->
                </el-table>
            </el-col>
            <el-col>
                <div style="padding: 15px; background-color: #fff;">

                    <el-pagination v-model:current-page="PageInfo.page" v-model:page-size="PageInfo.limit" background
                        :total="PageInfo.total" :page-sizes="[20, 50, 100]"
                        layout="total,sizes,prev, pager, next, jumper" @current-change="handleCurrentChange"
                        @size-change="handleSizeChange" />
                </div>
            </el-col>
        </el-row>

    </div>

    <el-dialog v-model="inviteDialog" title="邀请开通空间" width="500" align-center>
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
                    <el-input v-model="invitText" style="width: 240px" placeholder="邮箱地址 " clearable />
                </div>

            </el-col>
        </el-row>
        <el-row>
            <el-col>
                <div>
                    <el-input v-model="remarkText" type="textarea" style="width: 240px" placeholder="备注 " clearable />
                </div>

            </el-col>
        </el-row>
        <el-row>
            <el-col>
                <div v-if="invitUrl" style="border:#c9c9c9 2px dashed ; padding:5px;margin-top:5px"
                    @click="handleCopy(invitUrl, $event)">
                    点击复制邀请链接
                    <p>邀请链接：{{ invitUrl }}</p>
                </div>
            </el-col>
        </el-row>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="centerDialogVisible">取消</el-button>
                <el-button type="primary" @click="sendInvite" :disabled="buttonStatus">
                    发出邀请
                </el-button>
            </div>
        </template>
    </el-dialog>

    <el-dialog v-model="editRoles" title="修改权限" width="500" align-center>
        <el-row>
            <el-col style="margin-bottom:20px">
                <span>现在该用户权限为：{{ currEditRoleInfo.account_role == "owner" ? "空间所有者" : currEditRoleInfo.account_role ==
                    "admin"
                    ? "空间管理员" : "尊享会员" }}</span>
            </el-col>
        </el-row>
        <el-row style="margin-bottom: 20px;">
            修改为：
            <el-select v-model="newRole">
                <template v-for="item in rolesList" :key="item.key">
                    <el-option :label="item.value" :value="item.key" />
                </template>

            </el-select>
        </el-row>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="caneditRolesDialog">取消</el-button>
                <el-button type="primary" @click="putRoles">
                    确定
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue"
import { Plus, Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from "element-plus"
import { useRouter } from "vue-router"
import { inviteUser, members, memberChangeRole, memberRemove, getAuthList } from "@/api/api"
import clip from "@/utils/clipboard"
import MassInvite from "@/components/MassInvite/index.vue"
import { formatTime } from "@/utils"
import { useUserStore } from "@/store/modules/user"
const rolesList = ref([
    { key: "admin", value: "空间管理员" },
    { key: "normal", value: "尊享会员" }
])
const { token, roles } = useUserStore()
const workspaceRole = ref("")
const router = useRouter()
const tableData = ref([])
const inviteDialog = ref(false)
const invitText = ref("")
const remarkText = ref("")
const invitUrl = ref("")
const PageInfo = ref({
    "page": 1,
    "limit": 20,
    "total": 0,
    "keyword": ""

})
const buttonStatus = ref(false)
const newRole = ref("")
const editRoles = ref(false)
const currEditRoleInfo = ref({})
const handleCopy = (text, event) => {
    clip(text, event)
}

function handleCurrentChange() {
    authList()
}
function handleSizeChange() {
    authList()
}

function openInvite() {
    inviteDialog.value = true
    invitUrl.value = ""
    buttonStatus.value = false
}
const editRolesDialog = (arg) => {
    currEditRoleInfo.value = arg;
    console.log(arg);

    editRoles.value = true
}

const deleteDialog = (arg) => {

    ElMessageBox.confirm('是否删除该用户', '删除提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
    })
        .then(({ data }) => {
            memberRemove({ account_id: arg.id })
                .then(res => {
                    let { code, data, msg } = res.data
                    if (code == 0) {
                        ElMessage({
                            message: "删除成功 !",
                            type: "success",
                            duration: 3000,
                        })

                        authList()
                    } else {
                        ElMessage({
                            message: msg,
                            type: "error",
                            duration: 3000,
                        })
                    }
                })
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '取消删除',
            })
        })
}

const caneditRolesDialog = () => {
    editRoles.value = false
}
function putRoles() {
    let data = {
        account_id: currEditRoleInfo.value.id,
        role: newRole.value
    }
    memberChangeRole(data)
        .then(res => {
            let { code, data, msg } = res.data
            if (code == 0) {
                ElMessage({
                    message: "修改成功  !",
                    type: "success",
                    duration: 3000,
                })
                editRoles.value = false
            } else {
                ElMessage({
                    message: msg,
                    type: "error",
                    duration: 3000,
                })
            }
        })
}
function centerDialogVisible() {
    invitText.value = ""
    inviteDialog.value = false
}
function authList() {
    getAuthList(PageInfo.value).then(res => {
        let { code, msg, data } = res.data
        console.log(code, msg, data);

        if (code == 0) {
            tableData.value = data.data
            PageInfo.value.total = data.total
            PageInfo.value.page = data.page
            PageInfo.value.limit = data.limit
        } else {

            ElMessage({
                message: msg,
                type: "error",
                duration: 3000,
            })
        }


    })
}

function sendInvite() {

    if (roles == "superAdmin") {
        workspaceRole.value = "owner"
    } else if (workspaceRole.value == "") {
        ElMessage({
            message: "请选择邀请角色!",
            type: "error",
            duration: 3000,
        })
        return
    }

    inviteUser({
        email: invitText.value,
        domain: "racio.chat",
        role: workspaceRole.value,
        tenant_id: localStorage.getItem("tenant_id") || "",
        remark: remarkText.value

    })
        .then(res => {
            let { code, data, msg } = res.data
            if (code == 0) {
                invitUrl.value = data.url
                buttonStatus.value = true
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
            authList()
        })
}
onMounted(async () => {

    authList()
})
</script>
<style lang="scss" scoped>
.home-container {
    width: 98%;
    margin: 32px;
}

.image-slot {
    text-align: center;
    color: #ccc;
    font-size: 14px;
    margin-top: 10px;
}

@import "./index";
</style>
