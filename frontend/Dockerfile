FROM nginxinc/nginx-unprivileged:1.21.6-alpine

USER root
RUN apk update
RUN apk upgrade
RUN rm /etc/nginx/conf.d/default.conf
COPY ./dist /app
COPY ./nginx /etc/nginx
CMD nginx -g "daemon off;"

# Expose ports
EXPOSE 8080:8080
