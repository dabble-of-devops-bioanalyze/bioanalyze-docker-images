# Passing args to container here -
# https://www.jeffgeerling.com/blog/2017/use-arg-dockerfile-dynamic-image-specification

PANGEO_TAG?="2020.12.04"
RSTUDIO_VERSION?="1.3.107"
IMAGE?=base-image

build-docs:
	docker-compose build && \
		docker-compose up -d

up:
	docker-compose up

docs:
	docker-compose up -d

rebuild:
	docker-compose build --no-cache

jupyter-token:
	docker-compose logs jupyter | grep 127 | tail

build :
	cd $(IMAGE); \
	docker build -t $(IMAGE) \
		--build-arg PANGEO_TAG=${PANGEO_TAG} .

clean:
	docker-compose stop; docker-compose rm -v -f

clean-all :
	docker container stop $(docker container ls -aq); \
		docker system prune -f -a; \
		docker system prune -f -a --volumes

