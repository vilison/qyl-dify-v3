<template>
    <el-dropdown>
        <span class="el-dropdown-link">
            <el-avatar :size="30" class="avatar" :src="AvatarLogo" />
            {{ UserStore.userInfo.username }}-
            {{ currentRoles == "superAdmin" ? "Racio超级管理员" : currentRoles == "owner" ? "空间所有者" : "空间管理员" }}
            <el-icon class="header-icon el-icon--right">
                <arrow-down />
            </el-icon>
        </span>
        <template #dropdown>
            <el-dropdown-menu>
                <el-dropdown-item :command="3" divided @click="modifyPassword" v-if="currentRoles === 'superAdmin'">
                    <el-icon>
                        <Edit />
                    </el-icon>修改密码
                </el-dropdown-item>
                <el-dropdown-item :command="4" divided @click="logOut">
                    <el-icon>
                        <SwitchButton />
                    </el-icon>退出登录
                </el-dropdown-item>
            </el-dropdown-menu>
        </template>
    </el-dropdown>

    <PersonalDialog ref="person" />
</template>

<script lang="ts" setup>
import { useRouter } from "vue-router"
import { ElMessage, ElMessageBox } from "element-plus"
import { computed, ref } from "vue"

import AvatarLogo from "@/assets/image/avatar.png"
import { useTagsViewStore } from "@/store/modules/tagsView"
import { usePermissionStore } from "@/store/modules/permission"
import PersonalDialog from "./PersonalDialog.vue"
import path from 'path-browserify';
const router = useRouter()
const TagsViewStore = useTagsViewStore()
const PermissionStore = usePermissionStore()

import { useUserStore } from "@/store/modules/user"
const UserStore = useUserStore()
const currentRoles = computed({
    get() {
        return UserStore.roles[0]
    },
    set(val) {
        ; (async () => {
            await UserStore.getInfo([val])
            router.push({
                path: "/",
            })
            location.reload()
        })()
    },
})

const switchRolesAction = (type: string) => {
    if (type === currentRoles.value) return
    currentRoles.value = currentRoles.value === "admin" ? "other" : "admin"
}

// 用户信息
const userInfo = computed(() => UserStore.userInfo)
const person = ref()
const tenant = ref()

const logOut = async () => {
    ElMessageBox.confirm("您是否确认退出登录?", "温馨提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
    })
        .then(async () => {
            await UserStore.logout()
            await localStorage.clear()
            console.log(router.currentRoute.value.path, "router.currentRoute.value.path ");
            if (router.currentRoute.value.path.includes("/admin")) {
                await router.replace({ path: "/login" })
            } else {
                await router.replace({ path: "/auth" })
            }

            TagsViewStore.clearVisitedView()
            PermissionStore.clearRoutes()
            ElMessage({
                type: "success",
                message: "退出登录成功！",
            })
        })
        .catch(() => { })
}

const modifyPassword = () => {
    person.value.show()
}
</script>

<style lang="scss" scoped>
.avatar {
    margin-right: 6px;
}

.el-dropdown-link {
    cursor: pointer;
    //color: var(--el-color-primary);
    display: flex;
    align-items: center;
}
</style>
