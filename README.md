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

| name         | version   | pangeo_version   | python_version   | snakemake_version   | nextflow_version   | prefect_version   | airflow_version   | docker_image                                                                                                                                    |
|:-------------|:----------|:-----------------|:-----------------|:--------------------|:-------------------|:------------------|:------------------|:------------------------------------------------------------------------------------------------------------------------------------------------|
| cellprofiler | 4.1.3     | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/cellprofiler:cellprofiler-4.1.3--pangeo-2021.08.17--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0 |
| cellprofiler | 4.0.1     | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/cellprofiler:cellprofiler-4.0.1--pangeo-2021.08.17--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0 |
| cellprofiler | 4.1.3     | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/cellprofiler:cellprofiler-4.1.3--pangeo-2021.06.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0 |
| cellprofiler | 4.0.1     | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/cellprofiler:cellprofiler-4.0.1--pangeo-2021.06.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0 |
| cellprofiler | 4.1.3     | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/cellprofiler:cellprofiler-4.1.3--pangeo-2021.04.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0 |
| cellprofiler | 4.0.1     | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/cellprofiler:cellprofiler-4.0.1--pangeo-2021.04.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0 |
| conda_r      | 4.0.3     | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/conda_r:conda_r-4.0.3--pangeo-2021.08.17--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0           |
| conda_r      | 3.6.1     | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/conda_r:conda_r-3.6.1--pangeo-2021.08.17--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0           |
| conda_r      | 4.0.3     | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/conda_r:conda_r-4.0.3--pangeo-2021.06.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0           |
| conda_r      | 3.6.1     | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/conda_r:conda_r-3.6.1--pangeo-2021.06.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0           |
| conda_r      | 4.0.3     | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/conda_r:conda_r-4.0.3--pangeo-2021.04.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0           |
| conda_r      | 3.6.1     | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/conda_r:conda_r-3.6.1--pangeo-2021.04.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0           |
| scanpy       | 1.6.0     | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/scanpy:scanpy-1.6.0--pangeo-2021.08.17--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0             |
| scanpy       | 1.6.0     | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/scanpy:scanpy-1.6.0--pangeo-2021.06.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0             |
| scanpy       | 1.6.0     | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/scanpy:scanpy-1.6.0--pangeo-2021.04.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0             |
| napari       | 0.4.2     | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/napari:napari-0.4.2--pangeo-2021.08.17--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0             |
| napari       | 0.4.2     | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/napari:napari-0.4.2--pangeo-2021.06.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0             |
| napari       | 0.4.2     | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/napari:napari-0.4.2--pangeo-2021.04.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0             |
| seurat       | 4.0.0     | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/seurat:seurat-4.0.0--pangeo-2021.08.17--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0             |
| seurat       | 4.0.0     | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/seurat:seurat-4.0.0--pangeo-2021.06.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0             |
| seurat       | 4.0.0     | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/seurat:seurat-4.0.0--pangeo-2021.04.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0             |
| ml           | 1.0.0     | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/ml:ml-1.0.0--pangeo-2021.08.17--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0                     |
| ml           | 1.0.0     | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/ml:ml-1.0.0--pangeo-2021.06.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0                     |
| ml           | 1.0.0     | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/ml:ml-1.0.0--pangeo-2021.04.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0                     |
| stem_away_ml | 1.0.0     | 2021.08.17       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/stem_away_ml:stem_away_ml-1.0.0--pangeo-2021.08.17--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0 |
| stem_away_ml | 1.0.0     | 2021.06.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/stem_away_ml:stem_away_ml-1.0.0--pangeo-2021.06.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0 |
| stem_away_ml | 1.0.0     | 2021.04.05       | 3.8*             | 6.7.0               | 21.04.0            | 0.15.4            | 2.1.4             | dabbleofdevops/stem_away_ml:stem_away_ml-1.0.0--pangeo-2021.04.05--python-3.8--airflow-2.1.4--prefect-0.15.4--snakemake-6.7.0--nextflow-21.04.0 |



## Dask-gateway compatibility

(This information is completely grabbed from [Pangeo](https://github.com/pangeo-data/pangeo-docker-images#dask-gateway-compatibility))

If deploying in a Jupyterhub on Kubernetes cluster you'll need to make sure you're using the same pangeo versions.

| dask-gateway |  Pangeo Version tag  |
|--------------|-------------|
| 0.9          | 2020.11.06  |
| 0.8          | 2020.07.28  |
| 0.7          | 2020.04.22  |