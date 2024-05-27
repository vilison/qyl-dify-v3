## 说明
`Dockerfile` 上需要填写 3个关键的环境变量


`VITE_APP_BASE_API` account-api的域名路径  #注意必须跟account-api同域，除非支持跨域访问

`VITE_APP_WEBSITE` account-dashboard 该dashboard 的访问域名/路径

`VITE_APP_DIFY_URL`  dify前台的地址


改好`Dockerfile`上的配置 直接 build 就可以

参考
```
docker build -f ./Dockerfile -t 镜像路径/镜像名称 .
```