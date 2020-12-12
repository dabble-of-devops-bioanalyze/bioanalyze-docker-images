
# Passing args to container here -
# https://www.jeffgeerling.com/blog/2017/use-arg-dockerfile-dynamic-image-specification

PANGEO_TAG="2020.12.04"
RSTUDIO_VERSION="1.3.107"

base-notebook :
	cd pangeo-base-notebook; \
	docker build -t pangeo-base-notebook \
		--build-arg PANGEO_TAG=${PANGEO_TAG} .

cellprofiler :
	cd cellprofiler; \
	docker build -t cellprofiler
