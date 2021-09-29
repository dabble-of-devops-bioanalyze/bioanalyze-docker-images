## BioAnalyze Docker Images

These docker images are built to use as a part of a full stack Bioinformatics Analysis Environment. Each image can be used on it's own or as a part of a Jupyterhub Cluster.

Each image is meant to be a full fledged ecosystem for Bioinformatics. Images:

* Are fully ready to use with a [Jupyterhub](https://zero-to-jupyterhub.readthedocs.io/en/latest/) or [Dask Gateway Cluster](https://gateway.dask.org/install-kube.html).
* RStudio installed
* Jupyterlab installed
* Common software packages for data science such as Pandas, SciKit Learn, and TidyVerse
* Bioinformatics workflow runners: [Snakemake](https://snakemake.readthedocs.io/en/stable/) and [Nextflow](https://www.nextflow.io/).
* Workflow Orchestration systems: [Prefect](https://docs.prefect.io/#basic-installation) and [Airflow](https://airflow.apache.org/docs/apache-airflow/stable/start/local.html).
* Use the excellent [Pangeo Project](https://github.com/pangeo-data/pangeo-docker-images) as a base.
* Documentation packages such as [Jupyterbook](https://jupyterbook.org/) and [RBookdown](https://bookdown.org/).

[Bioinformatics Ecosystem](./docs/_source/_static/images/BioHub-Ecosystem-IDEs-and-Development-Environment.jpeg)

See each of the images at [Dockerhub](https://hub.docker.com/orgs/dabbleofdevops/repositories).



## Base Image: R: 4.0.3 RStudio: 1.2.5042 Conda: 4.9.2-0



### cellprofiler

[Cellprofiler](https://cellprofiler.org/) Free open-source software for measuring and analyzing cell images.


| name         | version   | docker_image                                                                                                                       | pangeo_version   | python_version   | snakemake_version   | nextflow_version   | prefect_version   | airflow_version   |
|:-------------|:----------|:-----------------------------------------------------------------------------------------------------------------------------------|:-----------------|:-----------------|:--------------------|:-------------------|:------------------|:------------------|
| cellprofiler | 4.1.3     | dabbleofdevops/cellprofiler:cellprofiler-4.1.3--pangeo-2021.08.17--python-3.8--cellprofiler-4.1.3--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| cellprofiler | 4.0.1     | dabbleofdevops/cellprofiler:cellprofiler-4.0.1--pangeo-2021.08.17--python-3.8--cellprofiler-4.0.1--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| cellprofiler | 4.1.3     | dabbleofdevops/cellprofiler:cellprofiler-4.1.3--pangeo-2021.06.05--python-3.8--cellprofiler-4.1.3--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| cellprofiler | 4.0.1     | dabbleofdevops/cellprofiler:cellprofiler-4.0.1--pangeo-2021.06.05--python-3.8--cellprofiler-4.0.1--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| cellprofiler | 4.1.3     | dabbleofdevops/cellprofiler:cellprofiler-4.1.3--pangeo-2021.04.05--python-3.8--cellprofiler-4.1.3--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| cellprofiler | 4.0.1     | dabbleofdevops/cellprofiler:cellprofiler-4.0.1--pangeo-2021.04.05--python-3.8--cellprofiler-4.0.1--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |



### conda_r

[R](https://www.r-project.org/) R is a free software environment for statistical computing and graphics.


| name    | version   | docker_image                                                                                                        | pangeo_version   | python_version   | snakemake_version   | nextflow_version   | prefect_version   | airflow_version   |
|:--------|:----------|:--------------------------------------------------------------------------------------------------------------------|:-----------------|:-----------------|:--------------------|:-------------------|:------------------|:------------------|
| conda_r | 4.0.3     | dabbleofdevops/conda_r:conda_r-4.0.3--pangeo-2021.08.17--python-3.8--conda_r-4.0.3--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| conda_r | 3.6.1     | dabbleofdevops/conda_r:conda_r-3.6.1--pangeo-2021.08.17--python-3.8--conda_r-3.6.1--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| conda_r | 4.0.3     | dabbleofdevops/conda_r:conda_r-4.0.3--pangeo-2021.06.05--python-3.8--conda_r-4.0.3--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| conda_r | 3.6.1     | dabbleofdevops/conda_r:conda_r-3.6.1--pangeo-2021.06.05--python-3.8--conda_r-3.6.1--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| conda_r | 4.0.3     | dabbleofdevops/conda_r:conda_r-4.0.3--pangeo-2021.04.05--python-3.8--conda_r-4.0.3--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| conda_r | 3.6.1     | dabbleofdevops/conda_r:conda_r-3.6.1--pangeo-2021.04.05--python-3.8--conda_r-3.6.1--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |



### scanpy

[Scanpy](https://scanpy.readthedocs.io/en/stable/) Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata.


| name   | version   | docker_image                                                                                                     | pangeo_version   | python_version   | snakemake_version   | nextflow_version   | prefect_version   | airflow_version   |
|:-------|:----------|:-----------------------------------------------------------------------------------------------------------------|:-----------------|:-----------------|:--------------------|:-------------------|:------------------|:------------------|
| scanpy | 1.6.0     | dabbleofdevops/scanpy:scanpy-1.6.0--pangeo-2021.08.17--python-3.8--scanpy-1.6.0--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| scanpy | 1.6.0     | dabbleofdevops/scanpy:scanpy-1.6.0--pangeo-2021.06.05--python-3.8--scanpy-1.6.0--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| scanpy | 1.6.0     | dabbleofdevops/scanpy:scanpy-1.6.0--pangeo-2021.04.05--python-3.8--scanpy-1.6.0--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |



### napari

[Napari](https://napari.org/) multi-dimensional image viewer for python.


| name   | version   | docker_image                                                                                                     | pangeo_version   | python_version   | snakemake_version   | nextflow_version   | prefect_version   | airflow_version   |
|:-------|:----------|:-----------------------------------------------------------------------------------------------------------------|:-----------------|:-----------------|:--------------------|:-------------------|:------------------|:------------------|
| napari | 0.4.2     | dabbleofdevops/napari:napari-0.4.2--pangeo-2021.08.17--python-3.8--napari-0.4.2--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| napari | 0.4.2     | dabbleofdevops/napari:napari-0.4.2--pangeo-2021.06.05--python-3.8--napari-0.4.2--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| napari | 0.4.2     | dabbleofdevops/napari:napari-0.4.2--pangeo-2021.04.05--python-3.8--napari-0.4.2--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |



### seurat

[Seurat](https://satijalab.org/seurat/) R Toolkit for single cell genomics.


| name   | version   | docker_image                                                                                                     | pangeo_version   | python_version   | snakemake_version   | nextflow_version   | prefect_version   | airflow_version   |
|:-------|:----------|:-----------------------------------------------------------------------------------------------------------------|:-----------------|:-----------------|:--------------------|:-------------------|:------------------|:------------------|
| seurat | 4.0.0     | dabbleofdevops/seurat:seurat-4.0.0--pangeo-2021.08.17--python-3.8--seurat-4.0.0--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| seurat | 4.0.0     | dabbleofdevops/seurat:seurat-4.0.0--pangeo-2021.06.05--python-3.8--seurat-4.0.0--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| seurat | 4.0.0     | dabbleofdevops/seurat:seurat-4.0.0--pangeo-2021.04.05--python-3.8--seurat-4.0.0--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |



### ml

The ML image hosts many different ML packages.


| name   | version   | docker_image                                                                                         | pangeo_version   | python_version   | snakemake_version   | nextflow_version   | prefect_version   | airflow_version   |
|:-------|:----------|:-----------------------------------------------------------------------------------------------------|:-----------------|:-----------------|:--------------------|:-------------------|:------------------|:------------------|
| ml     | 1.0.0     | dabbleofdevops/ml:ml-1.0.0--pangeo-2021.08.17--python-3.8--ml-1.0.0--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| ml     | 1.0.0     | dabbleofdevops/ml:ml-1.0.0--pangeo-2021.06.05--python-3.8--ml-1.0.0--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| ml     | 1.0.0     | dabbleofdevops/ml:ml-1.0.0--pangeo-2021.04.05--python-3.8--ml-1.0.0--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |



### stem_away_ml

The STEM Away ML image was build in collaboration with [STEMAway](https://stemaway.com/) for the Summer 2021 internship.

| name         | version   | docker_image                                                                                                                       | pangeo_version   | python_version   | snakemake_version   | nextflow_version   | prefect_version   | airflow_version   |
|:-------------|:----------|:-----------------------------------------------------------------------------------------------------------------------------------|:-----------------|:-----------------|:--------------------|:-------------------|:------------------|:------------------|
| stem_away_ml | 1.0.0     | dabbleofdevops/stem_away_ml:stem_away_ml-1.0.0--pangeo-2021.08.17--python-3.8--stem_away_ml-1.0.0--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| stem_away_ml | 1.0.0     | dabbleofdevops/stem_away_ml:stem_away_ml-1.0.0--pangeo-2021.06.05--python-3.8--stem_away_ml-1.0.0--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |
| stem_away_ml | 1.0.0     | dabbleofdevops/stem_away_ml:stem_away_ml-1.0.0--pangeo-2021.04.05--python-3.8--stem_away_ml-1.0.0--wms--a-2.1.4--p-0.15.4--s-6.7.0 | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             |





## Dask-gateway compatibility

(This information is completely grabbed from [Pangeo](https://github.com/pangeo-data/pangeo-docker-images#dask-gateway-compatibility))

If deploying in a Jupyterhub on Kubernetes cluster you'll need to make sure you're using the same pangeo versions.

| dask-gateway |  Pangeo Version tag  |
|--------------|-------------|
| 0.9          | 2020.11.06  |
| 0.8          | 2020.07.28  |
| 0.7          | 2020.04.22  |