# Usage

These docker images are built to be used in a Jupyterhub cluster, but can be run as is.

The docker images themselves are based on the [pangeo docker images](https://github.com/pangeo-data/pangeo-docker-images) project, and all images include RStudio Server in addition to JuptyerLab. 

## Zero to Kubernetes Usage

The [Zero to Kubernetes Project](https://zero-to-jupyterhub.readthedocs.io/) allows for [customizing user environments.](https://zero-to-jupyterhub.readthedocs.io/en/latest/jupyterhub/customizing/user-environment.html?#customizing-user-environment). Each user environment is backed by a docker image.

## Recommended Settings

I like to use the [DaskHub](https://github.com/dask/helm-chart/tree/master/daskhub) helm chart as the base configuration for my Jupyterhub Kubernetes cluster. It combines [Dask](https://dask.org/) plus the Zero to Kubernetes Project for general data science awesomeness.

## Adding Images to the Profile

You can add any number of images to the startup profile.

```
  singleuser:
    image:
      name: pangeo/base-notebook  # Image to use for singleuser environment. Must include dask-gateyway.
      tag: 2020.11.06
    defaultUrl: "/lab"  # Use jupyterlab by defualt.
  profileList:
   - display_name: "GPU Server"
     description: "Spawns a notebook server with access to a GPU"
     kubespawner_override:
       image: dabbleofdevops/ml-notebook:latest
       extra_resource_limits:
         nvidia.com/gpu: "1"
    - display_name: "CellProfiler Environment"
      description: "Free open-source software for measuring and analyzing cell images."
      kubespawner_override:
        image: dabbleofdevops/cellprofiler-notebook:latest
    - display_name: "Scanpy Environment"
      description: "Scanpy is a scalable toolkit for analyzing single-cell gene expression. Includes cellxgene."
      kubespawner_override:
        image: dabbleofdevops/scanpy-notebook:latest
```

## Single User Usage

These are docker images and can always be run individually.

```
docker run -it -p 8888:8888 \
    -v "$(pwd):/project" \
    dabbleofdevops/scanpy-notebook \
    bash -c "source activate notebook && jupyter notebook --ip 0.0.0.0 --allow-root"
```

Just the output for the token, and open `localhost:8888` and put in your token to start using jupyter notebook.


## Find Images

You can find all the images by either looking in the [github repo](https://github.com/Dabble-of-DevOps-Bio/dabble-of-devops-bioinformatics-jhub-docker) for `*-notebook` or looking on [Dockerhub](https://hub.docker.com/orgs/dabbleofdevops/repositories).

