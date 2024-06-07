#!/bin/bash

set -e
# 读取环境变量
APPID="${APPID:-default_app_id}"
GZHAPPID="${GZHAPPID:-default_gzhapp_id}"
BASE_API="${BASE_API:-default_base_api}"
WEBSITE="${WEBSITE:-default_website}"
DIFY_URL="${DIFY_URL:-default_dify_url}"
# 将环境变量注入到 index.html
sed -i "s|{{APPID}}|$APPID|g"  /usr/share/nginx/html/index.html
sed -i "s|{{BASE_API}}|$BASE_API|g"  /usr/share/nginx/html/index.html
sed -i "s|{{WEBSITE}}|$WEBSITE|g"  /usr/share/nginx/html/index.html
sed -i "s|{{DIFY_URL}}|$DIFY_URL|g"  /usr/share/nginx/html/index.html
sed -i "s|{{GZHAPPID}}|$GZHAPPID|g"  /usr/share/nginx/html/index.html

# 启动 Nginx

exec nginx -g 'daemon off;'
