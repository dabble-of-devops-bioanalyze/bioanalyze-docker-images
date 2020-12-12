# Passing args to container here -
# https://www.jeffgeerling.com/blog/2017/use-arg-dockerfile-dynamic-image-specification

PANGEO_TAG?="2020.12.04"
RSTUDIO_VERSION?="1.3.107"

IMAGE?=base-image
build :
	cd $(IMAGE); \
	docker build -t $(IMAGE) \
		--build-arg PANGEO_TAG=${PANGEO_TAG} .

