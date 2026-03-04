FROM nginx:alpine

# Remove default nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy your frontend build (html/css/js)
COPY . /usr/share/nginx/html/

# Expose web port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]