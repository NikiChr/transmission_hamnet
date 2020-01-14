FROM docker:dind

COPY content/ /

#coreutils for extra date options
RUN apk add --no-cache bash \
	py-pip \
	python-dev \
	libffi-dev \
	openssl-dev \
	gcc \
	libc-dev \
	git \
	musl-dev \
	go \
	curl \
	cvs \
	cmake \
	g++ \
	boost-dev \
	make \
	zlib-dev \
	openrc \
	coreutils \
	iproute2 \
	&& apk update \
	&& pip install docker-compose

# Transmission
RUN apk update \
	&& apk add transmission transmission-cli transmission-daemon

ENTRYPOINT dockerd --host=unix:///var/run/docker.sock --host=tcp://0.0.0.0:2375
CMD dockerd --host=unix:///var/run/docker.sock --host=tcp://0.0.0.0:2375
