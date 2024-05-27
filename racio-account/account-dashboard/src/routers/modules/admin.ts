/** When your routing table is too long, you can split it into small modules**/

import Layout from "@/layout/index.vue"

const adminRouter = [
    {
        path: "/admin",
        name: "admin",
        redirect: "/admin/home",
        hidden: false,
        component: Layout,
        meta: { title: "管理后台", tag: "superAdmin", roles: ["superAdmin"], icon: "House", requireAuth: true, },
        children: [
            {
                path: "/admin/home",
                component: () => import("@/views/admin/home.vue"),
                name: "home",
                meta: { title: "空间管理", icon: "House", requireAuth: true, roles: ["superAdmin"], tag: "superAdmin", },
            },
            {
                path: "/admin/list",
                component: () => import("@/views/admin/userList.vue"),
                name: "Userlist",
                meta: { title: "用户管理", icon: "House", requireAuth: true, roles: ["superAdmin"], tag: "superAdmin", },
            },
            {
                path: "/admin/invites",
                component: () => import("@/views/admin/invitesList.vue"),
                name: "invites",
                meta: { title: "邀请管理", icon: "Reading", requireAuth: true, roles: ["superAdmin"], tag: "superAdmin", },

            },
            {
                path: "/admin/apps",
                component: () => import("@/views/admin/apps.vue"),
                name: "apps",
                meta: {
                    title: "应用管理",
                    icon: "Reading",
                    requireAuth: true,
                    roles: ["superAdmin"], tag: "superAdmin",
                },

            },
        ]
    },
]

export default adminRouter
