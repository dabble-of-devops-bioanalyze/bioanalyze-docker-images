#  MLFlow and Running Services

The MLFlow examples comes from the [MlFlow Tutorials](https://www.mlflow.org/docs/latest/tutorials-and-examples/tutorial.html) with thanks.

In order to run this notebook you can either run as a part of a setup jupyterlab, or just run the docker image itself directly.

This is meant to be an example of how you can customize your software environments for your own needs, and also how to proxy services in JupyterHub.


```bash
# make sure to keep the ports consistent
docker run --rm -it -p 8004:8004 \
    dabbleofdevops/scanpy-notebook:latest \
    bash -c "jupyter notebook --ip 0.0.0.0 --port 8004"
```