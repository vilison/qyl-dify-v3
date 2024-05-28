FROM node:20.11-alpine3.19 AS base

RUN apk add --no-cache tzdata

WORKDIR /app/web
COPY . .



# ENV NODE_ENV "production"
# account-api 访问地址
ENV VITE_APP_BASE_API http://at-stg.racio.chat/api
#account-dashboard 访问地址
ENV VITE_APP_WEBSITE http://at-stg.racio.chat/dashboard
# dify平台访问地址
ENV VITE_APP_DIFY_URL http://dify.corp.chaolian360.com


RUN yarn install  --registry https://registry.npmmirror.com/

RUN yarn build


FROM nginx

# ENV TZ UTC
# RUN ln -s /usr/share/zoneinfo/${TZ} /etc/localtime \
#     && echo ${TZ} > /etc/timezone

COPY --from=base /app/web/dist/ /usr/share/nginx/html/
RUN rm /etc/nginx/conf.d/default.conf

COPY --from=base /app/web/docker/default.conf /etc/nginx/conf.d/
WORKDIR /usr/share/nginx/html/
