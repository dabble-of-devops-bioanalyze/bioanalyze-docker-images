ARG R_VER="4.0.3"

FROM rocker/r-ver:${R_VER}

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

# RStudio Stuff
# RStudio 1.3 used to work and now it doesn't
ARG RSTUDIO_VERSION
ENV RSTUDIO_VERSION=${RSTUDIO_VERSION:-1.2.5042}
ARG S6_VERSION
ARG DEBIAN_FRONTEND=noninteractive
ARG PANDOC_TEMPLATES_VERSION
ENV S6_VERSION=${S6_VERSION:-v1.21.7.0}
ENV S6_BEHAVIOUR_IF_STAGE2_FAILS=2
ENV PATH=/usr/lib/rstudio-server/bin:$PATH
ENV PANDOC_TEMPLATES_VERSION=${PANDOC_TEMPLATES_VERSION:-2.9}


ENV NB_PYTHON_PREFIX=${CONDA_DIR}/envs/${CONDA_ENV} \
    DASK_ROOT_CONFIG=${CONDA_DIR}/etc \
    HOME=/home/${NB_USER} \
    PATH=${CONDA_DIR}/bin:${PATH}

# ========================
## Install RStudio
## Download and install RStudio server & dependencies
## Attempts to get detect latest version, otherwise falls back to version given in $VER
## Symlink pandoc, pandoc-citeproc so they are available system-wide
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    curl vim-tiny vim-athena jq \
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
  && if [ -z "$RSTUDIO_VERSION" ]; \
    then RSTUDIO_URL="https://www.rstudio.org/download/latest/stable/server/bionic/rstudio-server-latest-amd64.deb"; \
    else RSTUDIO_URL="http://download2.rstudio.org/server/bionic/amd64/rstudio-server-${RSTUDIO_VERSION}-amd64.deb"; fi \
  && wget -q $RSTUDIO_URL \
  && dpkg -i rstudio-server-*-amd64.deb \
  && rm rstudio-server-*-amd64.deb \
  ## Symlink pandoc & standard pandoc templates for use system-wide
  && ln -s /usr/lib/rstudio-server/bin/pandoc/pandoc /usr/local/bin \
  && ln -s /usr/lib/rstudio-server/bin/pandoc/pandoc-citeproc /usr/local/bin \
  && git clone --recursive --branch ${PANDOC_TEMPLATES_VERSION} https://github.com/jgm/pandoc-templates \
  && mkdir -p /opt/pandoc/templates \
  && cp -r pandoc-templates*/* /opt/pandoc/templates && rm -rf pandoc-templates* \
  && mkdir /root/.pandoc && ln -s /opt/pandoc/templates /root/.pandoc/templates \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/ \
  ## RStudio wants an /etc/R, will populate from $R_HOME/etc
  && mkdir -p /usr/local/lib/R/etc/ \
  && touch  /usr/local/lib/R/etc/Rprofile.site \
  && mkdir -p /etc/R \
  ## Write config files in $R_HOME/etc
  && echo '\n\
    \n# Configure httr to perform out-of-band authentication if HTTR_LOCALHOST \
    \n# is not set since a redirect to localhost may not work depending upon \
    \n# where this Docker container is running. \
    \nif(is.na(Sys.getenv("HTTR_LOCALHOST", unset=NA))) { \
    \n  options(httr_oob_default = TRUE) \
    \n}' >> /usr/local/lib/R/etc/Rprofile.site \
  && echo "PATH=${PATH}" >> /usr/local/lib/R/etc/Renviron

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

RUN echo "Installing Apt-get packages..." \
    && apt-get update --fix-missing \
    && apt-get install -y apt-utils 2> /dev/null \
    && apt-get install -y wget zip libzmq3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*

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
        && rm -rf ${HOME}/.cache ${HOME}/.npm ${HOME}/.yarn \
        && rm -rf ${NB_PYTHON_PREFIX}/share/jupyter/lab/staging \
        && find ${CONDA_DIR} -follow -type f -name '*.a' -delete \
        && find ${CONDA_DIR} -follow -type f -name '*.pyc' -delete \
        && find ${CONDA_DIR} -follow -type f -name '*.js.map' -delete \
        ; fi

# ========================
# If they have a conda R this should bring up that R
# Otherwise it will just use the system R
ONBUILD RUN echo "Installing Python Jupyterhub + RStudio Magic..." \
        && export PATH=${NB_PYTHON_PREFIX}/bin:${PATH} \
        && conda install -c conda-forge -y \
            pip=20 jupyter-server-proxy jupyter_client \
        && pip install --no-cache-dir \
            jupyter-kite \
            jupyter-rsession-proxy \
            nbsphinx \
            jupyter-book \

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
ONBUILD RUN echo "Cleaning  /tmp" \
        && rm -rf /tmp/*

ONBUILD USER ${NB_USER}

USER ${NB_USER}
WORKDIR ${HOME}

ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}
