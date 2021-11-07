# Passing args to container here -
# https://www.jeffgeerling.com/blog/2017/use-arg-dockerfile-dynamic-image-specification

PANGEO_TAG?="2020.12.16"
RSTUDIO_VERSION?="1.2.5042"
IMAGE?=base-image

build-docs:
	docker-compose build && \
		docker-compose up -d

up:
	docker-compose up

docs:
	docker-compose up -d

rebuild:
	cd $(IMAGE); \
	docker build --no-cache -t $(IMAGE) .

jupyter-token:
	docker-compose logs jupyter | grep 127 | tail

# IMAGE=cellprofiler-notebook make build
build :
	cd $(IMAGE); \
	docker build -t $(IMAGE) .

clean:
	docker-compose stop; docker-compose rm -v -f
	find $(shell pwd) -name .ipynb_checkpoints -exec rm -rf {} \;
	find $(shell pwd) -name __pycache__ -exec rm -rf {} \;

clean-all :
	docker container stop $(docker container ls -aq); \
		docker system prune -f -a; \
		docker system prune -f -a --volumes

