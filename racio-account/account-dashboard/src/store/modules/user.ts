import { defineStore } from "pinia"

export const useUserStore = defineStore({
    // id: 必须的，在所有 Store 中唯一
    id: "userState",
    // state: 返回对象的函数
    state: () => ({
        // 登录token
        token: null,
        // 登录用户信息
        userInfo: {},
        isLogin: false,
        // 角色
        roles: localStorage.roles ? JSON.parse(localStorage.roles) : [],
        tenantId: localStorage.tenant_id || "",
        accessToken: localStorage.access_token || "",
        workspace_name: localStorage.workspace_name || "",
        workspace_id: localStorage.workspace_id || "",
    }),
    getters: {},
    // 可以同步 也可以异步
    actions: {
        // 登录
        login(userInfo) {
            console.log(userInfo, "userInfo");

            return new Promise(async (resolve, reject) => {
                this.userInfo = userInfo
                this.token = userInfo.token
                this.workspace_name = userInfo.workspace_name
                this.isLogin = true
                this.roles = userInfo.roles
                this.accessToken = userInfo.access_token
                this.tenantId = userInfo.tenant_id

                localStorage.setItem("token", userInfo.token)
                localStorage.setItem("workspace_name", userInfo.workspace_name)
                localStorage.setItem("roles", userInfo.roles)
                localStorage.setItem("access_token", userInfo.access_token || "")
                localStorage.setItem("tenant_id", userInfo.tenant_id || "")
                await this.getRoles(userInfo.roles)
                resolve(userInfo)
            })
        },
        // 获取用户授权角色信息，实际应用中 可以通过token通过请求接口在这里获取用户信息
        getRoles(roleType = "normal") {
            return new Promise((resolve, reject) => {
                // 获取权限列表 默认就是超级管理员，因为没有进行接口请求 写死
                this.roles = roleType  //roles角色 admin,owner, normal",
                localStorage.roles = JSON.stringify(this.roles)
                resolve(this.roles)
            })
        },
        // 获取用户信息 ，如实际应用中 可以通过token通过请求接口在这里获取用户信息
        getInfo(roles) {
            return new Promise((resolve, reject) => {
                this.roles = roles
                resolve(roles)
            })
        },
        // 退出
        logout() {
            return new Promise((resolve, reject) => {
                this.token = null
                this.userInfo = {}
                this.roles = []
                this.isLogin = false
                resolve(null)
            })
        },
    },
    // 进行持久化存储
    persist: {
        // 本地存储的名称
        key: "userState",
        //保存的位置
        storage: window.localStorage, //localstorage
    },
})
