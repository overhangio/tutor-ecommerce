# syntax=docker/dockerfile:1.4
###### Minimal image with base system requirements for most stages
FROM docker.io/ubuntu:20.04 AS minimal

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && \
    apt install -y curl git-core language-pack-en libmysqlclient-dev \
    libssl-dev libffi-dev build-essential 

ARG APP_USER_ID=1000
RUN useradd --home-dir /openedx --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

RUN mkdir /openedx/ecommerce_worker && \
    git clone https://github.com/openedx-unsupported/ecommerce-worker.git --branch open-release/sumac.master --depth 1 /openedx/ecommerce_worker
WORKDIR /openedx/ecommerce_worker

# Install pyenv
# https://www.python.org/downloads/
# https://github.com/pyenv/pyenv/releases
ARG PYTHON_VERSION=3.12.2
ENV PYENV_ROOT=/opt/pyenv
# root user is required for below 2 steps, as app user gets permission denied.
USER root
RUN git clone https://github.com/pyenv/pyenv $PYENV_ROOT --branch v2.3.36 --depth 1
# Install Python
RUN $PYENV_ROOT/bin/pyenv install $PYTHON_VERSION
USER app

# Create virtualenv
RUN $PYENV_ROOT/versions/$PYTHON_VERSION/bin/python -m venv ../venv/
ENV PATH=/openedx/venv/bin:$PATH
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install \
    # https://pypi.org/project/setuptools/
    # https://pypi.org/project/pip/
    # https://pypi.org/project/wheel/
    setuptools==69.1.1 pip==24.0 wheel==0.43.0
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install -r requirements/production.txt

ENV WORKER_CONFIGURATION_MODULE=ecommerce_worker.settings.production
CMD celery --app=ecommerce_worker.celery_app:app worker --loglevel=info --max-tasks-per-child=100 --queues=fulfillment,email_marketing
