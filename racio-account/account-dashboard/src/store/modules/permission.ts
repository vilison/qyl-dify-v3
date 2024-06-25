import { defineStore } from "pinia"
import { adminAsyncRoutes, accountAsyncRoutes, constantRoutes, routerArray, notFoundRouter } from "@/routers/index"
import { hasPermission, filterAsyncRoutes } from "@/utils/routers"
import { filterKeepAlive, filterRoutes } from "@/utils/routers"
export const usePermissionStore = defineStore({
    // id: 必须的，在所有 Store 中唯一
    id: "permissionState",
    // state: 返回对象的函数
    state: () => ({
        // 路由
        routes: [],
        // 动态路由
        addRoutes: [],
        // 缓存路由
        cacheRoutes: {},
    }),
    getters: {
        permission_routes: state => {
            return state.routes
        },
        keepAliveRoutes: state => {
            return filterKeepAlive(constantRoutes)
        },
    },
    // 可以同步 也可以异步
    actions: {
        // 生成路由
        generateRoutes(roles) {

            return new Promise(resolve => {
                // 在这判断是否有权限，哪些角色拥有哪些权限
                let accessedRoutes


                if (roles.includes("superAdmin")) {

                    accessedRoutes = filterAsyncRoutes(adminAsyncRoutes, roles)

                } else if (roles.includes("owner") || roles.includes("admin")) {

                    accessedRoutes = filterAsyncRoutes(accountAsyncRoutes, roles)

                } else {
                    accessedRoutes = []
                }
                console.log(accessedRoutes, "accessedRoutesaccessedRoutes");


                accessedRoutes = accessedRoutes.concat(notFoundRouter)
                this.routes = constantRoutes.concat(accessedRoutes)
                this.addRoutes = accessedRoutes

                resolve(accessedRoutes)
            })
        },
        // 清除路由
        clearRoutes() {
            this.routes = []
            this.addRoutes = []
            this.cacheRoutes = []
        },
        getCacheRoutes() {
            this.cacheRoutes = filterKeepAlive(constantRoutes)
            return this.cacheRoutes
        },
    },
})
