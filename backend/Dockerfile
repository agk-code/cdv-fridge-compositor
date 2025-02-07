FROM node@sha256:3ac002b133fd3737c44b66f0d023f5d75c7a1ddec71954fa06486aed6aead888

RUN mkdir -p /app
WORKDIR /app
COPY ./* /app
RUN npm install
RUN npm install redis
RUN npm install express
RUN npm install pg

CMD [ "npm", "run", "start" ]
