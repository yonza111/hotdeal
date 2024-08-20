# frontend/Dockerfile

# Stage 1: Build the React app
FROM node:20.14.0 AS build

WORKDIR /app

COPY ./frontend/package.json /app/package.json
COPY ./frontend/package-lock.json /app/package-lock.json

RUN yarn install

COPY ./frontend /app

RUN yarn build

# Stage 2: Serve the React app using nginx
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

