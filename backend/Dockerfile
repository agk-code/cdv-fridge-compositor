FROM node@sha256:3ac002b133fd3737c44b66f0d023f5d75c7a1ddec71954fa06486aed6aead888

WORKDIR /usr/app
COPY ./ /usr/app
RUN npm install && npm run fridge-backend
