/** When your routing table is too long, you can split it into small modules**/

import Layout from "@/layout/index.vue"

const accountRouter = [
    {
        path: "/account",
        name: "account",
        redirect: "/account/my",
        hidden: false,
        component: Layout,
        meta: { title: "管理后台", roles: ["owner", "admin"], icon: "House", requireAuth: true, },
        children: [
            {
                path: "/account/my",
                component: () => import("@/views/account/my.vue"),
                name: "my",
                meta: { title: "我的工作空间", icon: "House", requireAuth: true, roles: ["owner", "admin"] },
            },
            {
                path: "/account/list",
                component: () => import("@/views/account/list.vue"),
                name: "Userlist",
                meta: { title: "用户管理", icon: "House", requireAuth: true, roles: ["owner", "admin"] },
            },
            {
                path: "/account/invites",
                component: () => import("@/views/account/invitesList.vue"),
                name: "invites",
                meta: { title: "邀请管理", icon: "Reading", requireAuth: true, roles: ["owner", "admin"] },

            },
        ]
    },
]

export default accountRouter
