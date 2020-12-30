ARG R_VER="4.0.3"

FROM rocker/tidyverse:${R_VER}
#FROM rocker/tidyverse:3.6.3

# ----------------------
# We are clobbering together two docker files
# The rocker/binder file
# https://hub.docker.com/r/rocker/binder/dockerfile
# And the Pangeo Base
# https://github.com/pangeo-data/pangeo-docker-images/blob/master/base-image/Dockerfile
# ----------------------
USER root

# Run this section as root
# try to keep conda version in sync with repo2docker
# ========================
ENV CONDA_VERSION=4.9.2-0 \
    LD_LIBRARY_PATH=/usr/local/lib/R/lib \
    CONDA_ENV=notebook \
    NB_USER=jovyan \
    NB_UID=1000 \
    SHELL=/bin/bash \
    LANG=C.UTF-8  \
    LC_ALL=C.UTF-8 \
    CONDA_DIR=/srv/conda \
    DISABLE_AUTH=true

ENV NB_PYTHON_PREFIX=${CONDA_DIR}/envs/${CONDA_ENV} \
    DASK_ROOT_CONFIG=${CONDA_DIR}/etc \
    HOME=/home/${NB_USER} \
    PATH=${CONDA_DIR}/bin:${PATH}

# TODO Not sure this is a great idea.
# There are probably hard coded things in there
RUN echo "Updating rstudio user..." \
    && usermod -u 1001 rstudio \
    && groupmod -g 1001 rstudio

# Create jovyan user, permissions, add conda init to startup script
RUN echo "Creating ${NB_USER} user..." \
    && groupadd --gid ${NB_UID} ${NB_USER}  \
    && useradd --create-home --gid ${NB_UID} --no-log-init --uid ${NB_UID} ${NB_USER} \
    && echo ". ${CONDA_DIR}/etc/profile.d/conda.sh ; conda activate ${CONDA_ENV}" > /etc/profile.d/init_conda.sh \
    && chown -R ${NB_USER}:${NB_USER} /srv \
    && mkdir -p /home/${NB_USER}/.rstudio/monitored/user-settings \
    && echo 'alwaysSaveHistory="0" \
          \nloadRData="0" \
          \nsaveAction="0"' \
          > /home/${NB_USER}/.rstudio/monitored/user-settings/user-settings \
    && chown -R ${NB_USER}:${NB_USER} /home/${NB_USER}/.rstudio

# SEE: https://github.com/phusion/baseimage-docker/issues/58
ARG DEBIAN_FRONTEND=noninteractive

RUN echo "Installing Apt-get packages..." \
    && apt-get update --fix-missing \
    && apt-get install -y apt-utils 2> /dev/null \
    && apt-get install -y wget zip libzmq3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*

# RStudio with NO AUTH
RUN cp /etc/rstudio/disable_auth_rserver.conf /etc/rstudio/rserver.conf && \
	echo "USER=$NB_USER" >> /etc/environment

# ========================

USER ${NB_USER}
WORKDIR ${HOME}

RUN echo "Installing Miniforge..." \
    && URL="https://github.com/conda-forge/miniforge/releases/download/${CONDA_VERSION}/Miniforge3-${CONDA_VERSION}-Linux-x86_64.sh" \
    && wget --quiet ${URL} -O miniconda.sh \
    && /bin/bash miniconda.sh -u -b -p ${CONDA_DIR} \
    && rm miniconda.sh \
    && conda install -y -c conda-forge mamba \
    && mamba clean -afy \
    && find ${CONDA_DIR} -follow -type f -name '*.a' -delete \
    && find ${CONDA_DIR} -follow -type f -name '*.pyc' -delete

EXPOSE 8888
ENTRYPOINT ["/srv/start"]
#CMD ["jupyter", "notebook", "--ip", "0.0.0.0"]

# Only run these if used as a base image
# ----------------------
ONBUILD USER root
# hardcode for now
ONBUILD COPY --chown=jovyan:jovyan . /home/jovyan

ONBUILD RUN echo "Checking for 'binder' or '.binder' subfolder" \
        ; if [ -d binder ] ; then \
        echo "Using 'binder/' build context" \
        ; elif [ -d .binder ] ; then \
        echo "Using '.binder/' build context" \
        ; else \
        echo "Using './' build context" \
        ; fi

ONBUILD ARG DEBIAN_FRONTEND=noninteractive
ONBUILD RUN echo "Checking for 'apt.txt'..." \
        ; [ -d binder ] && cd binder \
        ; [ -d .binder ] && cd .binder \
        ; if test -f "apt.txt" ; then \
        apt-get update --fix-missing \
        && xargs -a apt.txt apt-get install -y \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* \
        ; fi

ONBUILD RUN echo "Cleaning out tmp" \
        rm -rf /tmp/*

ONBUILD USER ${NB_USER}

# Create "notebook" conda environment and dask labextensions
ONBUILD RUN echo "Checking for 'conda-linux-64.lock' or 'environment.yml'..." \
        ; [ -d binder ] && cd binder \
        ; [ -d .binder ] && cd .binder \
        ; if test -f "conda-linux-64.lock" ; then \
        mamba create --name ${CONDA_ENV} --file conda-linux-64.lock \
        ; elif test -f "environment.yml" ; then \
        mamba env create --name ${CONDA_ENV} -f environment.yml  \
        ; else echo "No conda-linux-64.lock or environment.yml! *creating default env*" ; \
        mamba create --name ${CONDA_ENV} pangeo-notebook \
        ; fi \
        && mamba clean -yaf \
        && find ${CONDA_DIR} -follow -type f -name '*.a' -delete \
        && find ${CONDA_DIR} -follow -type f -name '*.pyc' -delete \
        && find ${CONDA_DIR} -follow -type f -name '*.js.map' -delete \
        && find ${NB_PYTHON_PREFIX}/lib/python*/site-packages/bokeh/server/static -follow -type f -name '*.js' ! -name '*.min.js' -delete

# Install pip packages
# remove cache https://github.com/pypa/pip/pull/6391 ?
ONBUILD RUN echo "Checking for pip 'requirements.txt'..." \
        ; [ -d binder ] && cd binder \
        ; [ -d .binder ] && cd .binder \
        ; if test -f "requirements.txt" ; then \
        ${NB_PYTHON_PREFIX}/bin/pip install --no-cache-dir -r requirements.txt \
        ; fi

# Run postBuild script within "pangeo" environment
ONBUILD RUN echo "Checking for 'postBuild'..." \
        ; [ -d binder ] && cd binder \
        ; [ -d .binder ] && cd .binder \
        ; if test -f "postBuild" ; then \
        export PATH=${NB_PYTHON_PREFIX}/bin:${PATH} \
        && chmod +x postBuild \
        && ./postBuild \
        && rm -rf /tmp/* \
        && rm -rf ${HOME}/.cache ${HOME}/.npm ${HOME}/.yarn \
        && rm -rf ${NB_PYTHON_PREFIX}/share/jupyter/lab/staging \
        && find ${CONDA_DIR} -follow -type f -name '*.a' -delete \
        && find ${CONDA_DIR} -follow -type f -name '*.pyc' -delete \
        && find ${CONDA_DIR} -follow -type f -name '*.js.map' -delete \
        ; fi

# ========================
ONBUILD RUN echo "Installing Python Jupyterhub + RStudio Magic..." \
        && export PATH=${NB_PYTHON_PREFIX}/bin:${PATH} \
        && conda install -c conda-forge -y \
            pip=20 jupyter-server-proxy jupyter_client \
        && pip install --no-cache-dir \
            jupyter-rsession-proxy \
            nbsphinx \
            jupyter-book \
        && rm -rf /tmp/*

# Overwrite start entrypoint script if present
ONBUILD RUN echo "Checking for 'start'..." \
        ; [ -d binder ] && cd binder \
        ; [ -d .binder ] && cd .binder \
        ; if test -f "start" ; then \
        chmod +x start \
        && cp start /srv/start \
        ; fi
# ----------------------

ONBUILD USER root
#        && R --quiet -e "IRkernel::installspec(prefix='${CONDA_DIR}')" \
ONBUILD RUN echo "Installing R Jupyterhub + RStudio Magic..." \
        && export PATH=${NB_PYTHON_PREFIX}/bin:${PATH} \
        && R --quiet -e "devtools::install_github('IRkernel/IRkernel')" \
        && R --quiet -e "install.packages('rmarkdown')" \
        && rm -rf /tmp/* \
        && rstudio-server stop

ONBUILD USER ${NB_USER}

ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}
