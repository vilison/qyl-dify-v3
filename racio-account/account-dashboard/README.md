## 说明

docker-compose上的环境变量

APPID: ''  #微信网站扫描应用appid
GZHAPPID: ''  #微信公众号appid
BASE_API: '' # account-api 访问地址         #http://at-stg.racio.chat/api
WEBSITE: ' ' # account-dashboard 访问地址   #http://at-stg.racio.chat/dashboard
DIFY_URL: ' '  # dify平台访问地址            #http://dify.corp.chaolian360.com





参考
```
docker build -f ./Dockerfile -t 镜像路径/镜像名称 .
```


``` dify-nginx 容器 的default.conf 需要参考下面的config 去增加 dashboard的访问路径
location ^~ /account/ {
    proxy_pass http://127.0.0.1:8085/;  #这个换成容器内网络地址和端口 举例子：http://account-dashboard:80  http://容器名:容器内部端口号 ！！！注意！！！ dify-nginx 跟account-dashboard 必须是同一个虚拟网络。
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header REMOTE-HOST $remote_addr;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_http_version 1.1;
    add_header X-Cache $upstream_cache_status;
    add_header Cache-Control no-cache;
}
```