FROM nginx:1.25.3

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./ssl /etc/nginx/ssl

EXPOSE 80 443 443/udp

CMD ["nginx", "-g", "daemon off;"]
