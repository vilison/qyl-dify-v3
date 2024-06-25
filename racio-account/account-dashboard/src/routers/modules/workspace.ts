/** When your routing table is too long, you can split it into small modules**/

import Layout from "@/layout/index.vue"

const workspaceRouter = [
    {
        path: "/workspace",
        name: "workspace",
        redirect: "/workspace/my",
        hidden: false,
        component: Layout,
        meta: { title: "管理后台", roles: ["owner", "admin"], icon: "House", requireAuth: true, },
        children: [
            {
                path: "/workspace/my",
                component: () => import("@/views/workspace/my.vue"),
                name: "my",
                meta: { title: "我的工作空间", icon: "House", requireAuth: true, roles: ["owner", "admin"] },
            },
            {
                path: "/workspace/list",
                component: () => import("@/views/workspace/list.vue"),
                name: "Userlist",
                meta: { title: "用户管理", icon: "House", requireAuth: true, roles: ["owner", "admin"] },
            },
            {
                path: "/workspace/invites",
                component: () => import("@/views/workspace/invitesList.vue"),
                name: "invites",
                meta: { title: "邀请管理", icon: "Reading", requireAuth: true, roles: ["owner", "admin"] },

            },
        ]
    },
]

export default workspaceRouter
