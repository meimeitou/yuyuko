FROM hub.dns.360.cn/library/node:15.14.0

COPY . .
RUN yarn install --registry=https://registry.npm.taobao.org

RUN apk add make \
    && make build

FROM hub.dns.360.cn/dns/nginx-worker:1.18

WORKDIR /app

COPY default.conf /etc/nginx/conf.d/default.conf
COPY --from=0 /dist /etc/nginx/dist

RUN set -xe \
    && apk add logrotate gzip \
    && chown -R nobody:nobody /etc/nginx/dist 
