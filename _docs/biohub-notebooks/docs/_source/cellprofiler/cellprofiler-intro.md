#  High Content Screening Analysis with CellProfiler

The cellprofiler example notebook came from the [cellprofiler notebooks repo](https://github.com/CellProfiler/notebooks/blob/master/cellprofiler_demo.ipynbs) with thanks. The only changes that were made were fix some import errors for CellProfiler v4.

In order to run this notebook you can either run as a part of a setup jupyterlab, or just run the docker image itself directly.


```bash
# make sure to keep the ports consistent
docker run --rm -it -p 8004:8004 \
    dabbleofdevops/cellprofiler:latest \
    bash -c "jupyter notebook --ip 0.0.0.0 --port 8004"
```