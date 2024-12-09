# syntax=docker/dockerfile:1.4
###### Minimal image with base system requirements for most stages
FROM docker.io/ubuntu:20.04 AS minimal

ENV DEBIAN_FRONTEND=noninteractive
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && \
    apt install -y curl gettext git-core language-pack-en

###### Checkout code
FROM minimal AS checkout

ARG ECOMMERCE_REPOSITORY=https://github.com/openedx-unsupported/ecommerce.git
ARG ECOMMERCE_VERSION='open-release/sumac.master'
RUN mkdir -p /openedx/ecommerce && \
    git clone $ECOMMERCE_REPOSITORY --branch $ECOMMERCE_VERSION --depth 1 /openedx/ecommerce

# Identify tutor user to cherry-pick commits
RUN git config --global user.email "tutor@overhang.io" \
  && git config --global user.name "Tutor"

##### Empty layer with just the repo at the root.
# This is useful when overriding the build context with a host repo:
# docker build --build-context /path/to/ecommerce
FROM scratch AS ecommerce-src
COPY --from=checkout /openedx/ecommerce /

###### Install python and virtual environment
FROM minimal AS python

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && \
    apt install -y libmysqlclient-dev libssl-dev build-essential \
    libsqlite3-dev libffi-dev mime-support pkg-config

ARG APP_USER_ID=1000
RUN if [ "$APP_USER_ID" = 0 ]; then echo "app user may not be root" && false; fi
RUN useradd --home-dir /openedx --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

# Create cache dir. Otherwise, for some reason, it becomes owned by root.
RUN mkdir /openedx/.cache

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
RUN $PYENV_ROOT/versions/$PYTHON_VERSION/bin/python -m venv /openedx/venv
ENV PATH=/openedx/venv/bin:$PATH
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared,uid=${APP_USER_ID} pip install \
    # https://pypi.org/project/setuptools/
    # https://pypi.org/project/pip/
    # https://pypi.org/project/wheel/
    setuptools==69.1.1 pip==24.0 wheel==0.43.0

# Install a recent version of nodejs
# https://pypi.org/project/nodeenv
RUN pip install nodeenv==1.8.0
RUN nodeenv /openedx/nodeenv --node=16.20.0 --prebuilt
ENV PATH=/openedx/nodeenv/bin:${PATH}

# Copy ecommerce source code
COPY --from=ecommerce-src --chown=app:app / /openedx/ecommerce
WORKDIR /openedx/ecommerce

# Install npm, bower requirements
ARG NPM_REGISTRY='{{ NPM_REGISTRY }}'
RUN --mount=type=cache,target=/openedx/.npm/,sharing=shared,uid=${APP_USER_ID} npm clean-install --verbose --no-audit --registry=$NPM_REGISTRY
RUN --mount=type=cache,target=/openedx/.cache/bower,sharing=shared,uid=${APP_USER_ID} node_modules/.bin/bower install --allow-root

# python requirements
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared,uid=${APP_USER_ID} pip install -r requirements.txt
# https://pypi.org/project/uWSGI/
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared,uid=${APP_USER_ID} pip install uwsgi==2.0.27

# Install private requirements: this is useful for installing custom payment processors.
COPY --chown=app:app ./requirements/ /openedx/requirements
RUN cd /openedx/requirements/ \
  && touch ./private.txt \
  && pip install -r ./private.txt

{% for extra_requirement in ECOMMERCE_EXTRA_PIP_REQUIREMENTS %}RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared,uid=${APP_USER_ID} pip install '{{ extra_requirement }}'
{% endfor %}

RUN atlas pull --repository="{{ ATLAS_REPOSITORY }}" --revision="{{ ATLAS_REVISION }}" {{ ATLAS_OPTIONS }} translations/ecommerce/ecommerce/conf/locale:ecommerce/conf/locale
RUN python manage.py compilemessages

{{ patch("ecommerce-dockerfile-pre-assets") }}

# Collect static assets (aka: "make static")
COPY --chown=app:app assets.py ./ecommerce/settings/assets.py
ENV DJANGO_SETTINGS_MODULE=ecommerce.settings.assets
RUN python3 manage.py update_assets --skip-collect
RUN ./node_modules/.bin/r.js -o build.js
RUN python3 manage.py collectstatic --noinput
RUN python3 manage.py compress --force

# Setup minimal yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV ECOMMERCE_CFG=/openedx/config.yml

EXPOSE 8000
CMD uwsgi \
    --static-map /static=/openedx/ecommerce/assets \
    --static-map /media=/openedx/ecommerce/course_ecommerce/media \
    --http 0.0.0.0:8000 \
    --thunder-lock \
    --single-interpreter \
    --enable-threads \
    --processes=2 \
    --buffer-size=8192 \
    --wsgi-file ecommerce/wsgi.py
