FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY pages /usr/share/nginx/html/pages
COPY js /usr/share/nginx/html/js
COPY components /usr/share/nginx/html/components

EXPOSE 80