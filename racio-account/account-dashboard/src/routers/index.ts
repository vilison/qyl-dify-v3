import {
    createRouter,
    createWebHistory,
    RouteRecordRaw,
    createWebHashHistory,
    Router,
} from "vue-router"
import Layout from "@/layout/index.vue"
import store from '@/store'
import adminRouter from "./modules/admin"
import workspaseRouter from "./modules/workspace"
import { storeToRefs } from 'pinia'
import { useUserStore } from "@/store/modules/user"
// 扩展继承属性
interface extendRoute {
    hidden?: boolean
}
//


// 异步组件
export const adminAsyncRoutes = [
    ...adminRouter,
]

export const accountAsyncRoutes = [
    ...workspaseRouter,

]

/**
 * path ==> 路由路径
 * name ==> 路由名称
 * component ==> 路由组件
 * redirect ==> 路由重定向
 * alwaysShow ==> 如果设置为true，将始终显示根菜单，无论其子路由长度如何
 * hidden ==> 如果“hidden:true”不会显示在侧边栏中（默认值为false）
 * keepAlive ==> 设为true 缓存
 * meta ==> 路由元信息
 * meta.title ==> 路由标题
 * meta.icon ==> 菜单icon
 * meta.affix ==> 如果设置为true将会出现在 标签栏中
 * meta.breadcrumb ==> 如果设置为false，该项将隐藏在breadcrumb中（默认值为true）
 * meta.activeMenu ==> 详情页的时候可以设置菜单高亮 ,高亮菜单的path
 */

export const constantRoutes: Array<RouteRecordRaw & extendRoute> = [
    {
        path: "/404",
        name: "404",
        component: () => import("@/views/errorPages/404.vue"),
        meta: { title: "外星人掳走了页面" },
        hidden: true,
    },
    {
        path: "/403",
        name: "403",
        component: () => import("@/views/errorPages/403.vue"),
        hidden: true,
    },
    {
        path: "/invitSuccess",
        name: "invitSuccess",
        component: () => import("@/views/success/invitSuccess.vue"),
        hidden: true,
    },
    {
        path: "/auth",
        name: "Auth",
        hidden: true,
        redirect: "/auth/index",
        meta: { title: "扫码登录" },
        children: [
            {
                path: "/auth/index",
                name: "auth",
                component: () => import("@/views/auth/auth.vue"),
                meta: { title: "微信登陆" },
            },
            {
                path: "/auth/check",
                name: "wxcheck",
                component: () => import("@/views/auth/check.vue"),
                meta: { title: "checking" },
            },
            {
                path: "/auth/gzhcheck",
                name: "gzhcheck",
                component: () => import("@/views/auth/gzhcheck.vue"),
                meta: { title: "gzhchecking" },
            }
        ]
    },
    {
        path: "/workspace",
        name: "workspace",
        redirect: "/workspace/my",
        component: Layout,
        hidden: true,
        meta: { title: "空间管理后台", requireAuth: true, roles: ["owner", "admin"], tag: "user", },
        children: [
        ]
    },
    {
        path: "/admin",
        name: "admin",
        // redirect: "/admin/home",
        hidden: true,
        component: Layout,
        meta: { title: "系统管理后台", requireAuth: true, roles: ["superAdmin"], tag: "superAdmin", },
        children: [

        ]
    },
    {
        path: "/login",
        name: "Login",
        component: () => import("@/views/login/index.vue"),
        hidden: true,
        meta: { title: "管理员登录" },
    },
    {
        path: "/logout",
        name: "Logout",
        component: () => import("@/views/logout/index.vue"),
        hidden: true,
        meta: { title: "退出登录" },
    },
    {
        path: "/activate",
        name: "Activate",
        redirect: "/activate/index",
        hidden: true,
        meta: { title: "激活邀请" },
        children: [
            {
                path: "/activate/index",
                component: () => import("@/views/activate/index.vue"),
                name: "activate",
                meta: { title: "激活邀请", icon: "Phone" },
            },
            {
                path: "/activate/phone",
                component: () => import("@/views/activate/phone.vue"),
                name: "phone",
                meta: { title: "绑定手机", icon: "Phone" },
            },
            {
                path: "/activate/gzhphone",
                component: () => import("@/views/activate/gzhphone.vue"),
                name: "gzhphone",
                meta: { title: "绑定手机", icon: "Phone" },
            },
        ]
    },
    {
        path: "/",
        name: "layout",
        hidden: true,
        component: () => import("@/views/auth/index.vue"),
        meta: { title: "首页", icon: "House" },
        children: []
    },
]

/**
 * notFoundRouter(找不到路由)
 */
export const notFoundRouter = {
    path: "/:pathMatch(.*)",
    name: "notFound",
    redirect: "/404",
}



const router = createRouter({
    history: createWebHistory(import.meta.env.MODE === "production" ? "/account" : "/"), // history
    // history: createWebHashHistory(), // hash
    routes: constantRoutes,
})


export default router
