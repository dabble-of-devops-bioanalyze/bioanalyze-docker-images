FROM  jupyter/minimal-notebook:6d42503c684f

# https://hub.docker.com/r/rocker/rstudio/dockerfile

USER root

WORKDIR /tmp

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y; apt-get upgrade -y; \
    apt-get install -y curl vim-tiny vim-athena jq; \
    apt-get install -y --no-install-recommends \
    uuid \
    file \
    git \
    libapparmor1 \
    libclang-dev \
    libcurl4-openssl-dev \
    libedit2 \
    libssl-dev \
    lsb-release \
    psmisc \
    procps \
    python-setuptools \
    sudo \
    wget \
    libxkbcommon-x11-0 \
    libedit2 r-base gdebi-core && \
    wget https://download1.rstudio.org/desktop/bionic/amd64/rstudio-1.3.1073-amd64.deb && \
    wget https://download2.rstudio.org/server/bionic/amd64/rstudio-server-1.3.1073-amd64.deb && \
    dpkg -i rstudio-1.3.1073-amd64.deb && \
    dpkg -i rstudio-server-1.3.1073-amd64.deb && \
    rm -rf /var/lib/apt/lists/*

USER $NB_UID

# Jupyterhub session proxy
RUN pip install jupyter-rsession-proxy
RUN conda install -c conda-forge r-base r-essentials jupyter-server-proxy && \
    conda clean --all -f -y

RUN jupyter labextension install @jupyterlab/server-proxy && \
    jupyter serverextension enable --sys-prefix jupyter_server_proxy

RUN fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

USER root

COPY ./custom-fix-permissions.sh /tmp/custom-fix-permissions.sh

RUN chmod 777 /tmp/custom-fix-permissions.sh && \
    /tmp/custom-fix-permissions.sh

USER $NB_USER

WORKDIR /home/${NB_USER}

# Dask
#RUN conda install -c conda-forge dask dask-ml dask-labextension && \
#    conda clean --all -f -y && \
#    fix-permissions "${CONDA_DIR}" && \
#    fix-permissions "/home/${NB_USER}"
#
#RUN jupyter labextension install dask-labextension && \
#    jupyter serverextension enable dask_labextension
#
