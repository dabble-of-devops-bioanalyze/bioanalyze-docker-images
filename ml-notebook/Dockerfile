ARG PANGEO_TAG=2020.12.04

FROM pangeo/ml-notebook:${PANGEO_TAG}

USER root

ARG RSTUDIO_VERSION=1.3.1073
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /tmp

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
    rm -rf /var/lib/apt/lists/* && \
    rm -rf rstudio*.deb

# Setup R environmental variables
# https://github.com/jupyterhub/jupyter-rsession-proxy/blob/master/jupyter_rsession_proxy/__init__.py#L48
#'R --slave --vanilla -e 'cat(paste(R.home("home"),R.home("share"),R.home("include"),R.home("doc"),getRversion(),sep=":"))' '
#        R_HOME, R_SHARE_DIR, R_INCLUDE_DIR, R_DOC_DIR, version = \
#            r_output.decode().split(':')
# Get the output and add those to these variables
#/usr/lib/R:/usr/share/R/share:/usr/share/R/include:/usr/share/R/doc:3.4.4

USER ${NB_USER}
WORKDIR ${HOME}

ENV R_HOME "/usr/lib/R"
ENV R_SHARE_DIR "/usr/share/R/share"
ENV R_INCLUDE_DIR "/usr/share/R/include"
ENV R_DOC_DIR "/usr/share/R/doc"

ENV RSTUDIO_DEFAULT_R_VERSION_HOME "/usr/lib/R"
ENV RSTUDIO_DEFAULT_R_VERSION "3.4.4"

ENV USER ${NB_USER}
