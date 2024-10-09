
FROM nginx:alpine

## Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# # Replace with our own nginx.conf
COPY nginx.conf /etc/nginx/conf.d/
# # 複製 SSL 憑證和密鑰
# COPY ssl.crt /etc/nginx/ssl.crt
# COPY ssl.key /etc/nginx/ssl.key
# COPY ssl.csr /etc/nginx/ssl.csr

# EXPOSE 443


