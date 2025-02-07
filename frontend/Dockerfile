FROM nginx@sha256:4d5c9a3437fc6b4d886c7c65ca59a1851120e9e63a4951a7d7cb7a4155501383

RUN mkdir -p /data
RUN mkdir -p /data/www
WORKDIR /data/www
COPY ./* /data/www
