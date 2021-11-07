#  Single Cell Analysis with Scanpy

The scanpy example notebooks come from the [scanpy tutorial repo](https://github.com/theislab/scanpy-tutorials) with thanks.

In order to run this notebook you can either run as a part of a setup jupyterlab, or just run the docker image itself directly.


```bash
# make sure to keep the ports consistent
docker run --rm -it -p 8004:8004 \
    dabbleofdevops/scanpy-notebook:latest \
    bash -c "jupyter notebook --ip 0.0.0.0 --port 8004"
```