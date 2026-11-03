# Build stage: compile Tailwind CSS
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY tailwind.config.js ./
COPY src ./src
COPY index.html ./
RUN npm run build:css

# Final stage: static site served by nginx
FROM nginx:1.29-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html
COPY --from=builder /app/styles.css /usr/share/nginx/html/styles.css
COPY logo.png /usr/share/nginx/html/logo.png
COPY robots.txt /usr/share/nginx/html/robots.txt
COPY sitemap.xml /usr/share/nginx/html/sitemap.xml
COPY assets /usr/share/nginx/html/assets
