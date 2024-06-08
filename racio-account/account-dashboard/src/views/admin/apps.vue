<template>

    <div class="home-container">
        <el-row class="row-bg" :gutter="11">

            <el-col :span="24">
                <el-table :data="tableData" style="width: 100%">
                    <el-table-column type="index" prop="date" label="应用编号" min-width="160" />
                    <el-table-column prop="id" label="用户ID" width="300" />
                    <el-table-column prop="status" label="状态" width="100" />

                    <el-table-column prop="created_at" label="创建时间" width="150">
                        <template #default="scope">
                            <div>{{ formatTime(scope.row.created_at, "") }}</div>
                        </template>
                    </el-table-column>

                    <el-table-column label="操作" fixed="right" width="200">
                        <template #default="scope">
                            <el-button type="primary">审核</el-button>
                            <el-button type="danger">停用</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-col>
            <el-col>
                <div style="padding: 15px;background-color: #fff;">



                    <el-pagination v-model:current-page="PageInfo.page" v-model:page-size="PageInfo.limit" background
                        :total="PageInfo.total" @current-change="handleCurrentChange" />
                </div>
            </el-col>
        </el-row>

    </div>

    <el-dialog v-model="inviteDialog" title="邀请开通空间" width="500" align-center>
        <span>输入被邀请人邮箱，如空则只生成邀请链接</span>
        <div>
            <el-input v-model="invitText" style="width: 240px" placeholder="邮箱地址 " clearable />
        </div>
        <div v-if="invitUrl" style="border:#c9c9c9 2px dashed ; padding:5px;margin-top:5px"
            @click="handleCopy(invitUrl, $event)">
            点击复制邀请链接
            <p>邀请链接：{{ invitUrl }}</p>
        </div>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="centerDialogVisible">取消</el-button>
                <el-button type="primary" @click="sendInvite">
                    发出邀请
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue"
import { ElMessage } from "element-plus"
import { useRouter } from "vue-router"

import { getAuthList, } from "@/api/api"
import clip from "@/utils/clipboard"
import { formatTime } from "@/utils"

let token = localStorage.getItem('token')
const router = useRouter()
const tableData = ref([])
const inviteDialog = ref(false)
const invitText = ref("")
const invitUrl = ref("")
const PageInfo = ref({
    "page": 1,
    "limit": 10,
    "total": 0
})
const handleCopy = (text, event) => {
    clip(text, event)
}

function handleCurrentChange() {
    AuthList()
}

function openInvite() {
    inviteDialog.value = true
}
function centerDialogVisible() {
    invitText.value = ""
    inviteDialog.value = false
}
function AuthList() {
    getAuthList(PageInfo.value).then(res => {
        let { code, msg, data } = res.data

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
    inviteUser({
        email: invitText.value,
        language: "zh-Hans",
        domain: "racio.chat",
        // role: "owener"

    })
        .then(res => {
            let { code, data, msg } = res.data
            if (code == 0) {
                invitUrl.value = data.url
            }
        })
        .catch(error => {
            ElMessage({
                message: error.message,
                type: "error",
                duration: 3000,
            })
        })
}
onMounted(async () => {

    // AuthList()
})
</script>
<style lang="scss" scoped>
.home-container {
    width: 90%;
    margin: 32px;
}

@import "./index";
</style>
