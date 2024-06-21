import request from "./request"


// 超级管理员登录
export function login(data) {
    return request({
        url: "/web/login",
        method: "post",
        data,
    })
}


// 超级管理员，空间管理账号列表
export function getAuthList(data) {
    return request({
        url: "/web/accounts",
        method: "post",
        data,
    })
}

/*
{
    "email": "xxx@df.com",
    "language": "zh-Hans"
}
 */
export function inviteUser(data) {
    return request({
        url: "/web/member_invites/invite-email",
        method: "post",
        data,
    })
}

/*
获取空间里的所有账号
 */
export function members(data) {
    return request({
        url: "/web/members",
        method: "post",
        data,
    })

}

// 修改密码 密码格式 英文大小写数字8位 r"^(?=.*[a-zA-Z])(?=.*\d).{8,}$"
export function editPassword(data) {
    return request({
        url: "/web/accounts/update_pwd",
        method: "post",
        data,
    })
}

//邀请列表
export function memberInvites(data) {
    return request({
        url: "/web/member_invites",
        method: "post",
        data,
    })

}


//获取当前登录账号的所有空间
export function accountTenantList() {
    return request({
        url: "/web/tenant/list",
        method: "post",
    })
}

// 切换空间
export function tenantSwitch(data) {
    return request({
        url: "/web/tenant/switch",
        method: "post",
        data
    })
}
// 当前空间移除用户
export function memberRemove(data) {
    return request({
        url: "/web/member/remove",
        method: "post",
        data,
    })
}
// 变更用户角色
export function memberChangeRole(data) {
    return request({
        url: "/web/member/update_role",
        method: "post",
        data,
    })
}

// 根据access_token 获取用户jwt_token
export function getJwtToken(data) {
    return request({
        url: "/console/account/get_token",
        method: "post",
        data,
    })
}


// 微信授权获取access_token
export function getWxInfo(data) {
    return request({
        url: "/console/oauth/access_token/wx",
        method: "post",
        data,
    })
}

// 微信公众号授权获取access_token
export function getGZHInfo(data) {
    return request({
        url: "/console/oauth/access_token/wechat",
        method: "post",
        data,
    })
}


// 激活状态验证
export function checkInvitToken(data) {
    return request({
        url: "/console/activate/check",
        method: "post",
        data,
    })
}

// 发送短信
export function sendSms(data) {
    return request({
        url: "/console/sms/send",
        method: "post",
        data,
    })
}



// 激活提交
export function activate(data) {
    return request({
        url: "/console/activate",
        method: "post",
        data,
    })
}

// 检查openid是否已存在
export function checkOpenId(data) {
    return request({
        url: "/console/account/check",
        method: "post",
        data,
    })
}
export function hasOwnerTenant(data) {
    return request({
        url: "/console/activate/create_check",
        method: "post",
        data,
    })
}