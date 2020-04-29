FROM  node:14.0.0-buster as node
LABEL maintainer="criss1913@gmail.com"

# setting up working directory
RUN mkdir /app
WORKDIR /app

# Install app dependencies then all files
COPY ./package.json ./package-lock.json /app/
RUN npm install

# Build app
COPY . .
RUN npm run build --prod

# nginx install
FROM nginx:mainline

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy output to nginx
COPY --from=node /app/dist/angular /usr/share/nginx/html

# Copy nginx configuration file.
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf