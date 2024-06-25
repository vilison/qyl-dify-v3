FROM node:20.11-alpine3.19  AS base



WORKDIR /app/web/
COPY . .
RUN rm -rf .yarn
RUN rm -rf node_modules

RUN yarn config set registry https://registry.npmmirror.com


RUN yarn install
RUN yarn build


FROM nginx

# ENV TZ UTC
# RUN ln -s /usr/share/zoneinfo/${TZ} /etc/localtime \
#     && echo ${TZ} > /etc/timezone
WORKDIR /usr/share/nginx/html/

COPY --from=base /app/web/dist/ /usr/share/nginx/html/
RUN rm /etc/nginx/conf.d/default.conf

COPY --from=base /app/web/docker/default.conf /etc/nginx/conf.d/
COPY --from=base /app/web/docker/entrypoint.sh ./entrypoint.sh


EXPOSE 3001
ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]