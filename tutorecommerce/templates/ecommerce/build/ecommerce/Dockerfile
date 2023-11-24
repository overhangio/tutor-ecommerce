{% if is_buildkit_enabled() %}# syntax=docker/dockerfile:1.4{% endif %}
###### Minimal image with base system requirements for most stages
FROM docker.io/ubuntu:20.04 as minimal

RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked{% endif %} \
    apt update && \
    apt install -y curl git-core language-pack-en

###### Checkout code
FROM minimal as checkout

ARG ECOMMERCE_REPOSITORY=https://github.com/edx/ecommerce.git
ARG ECOMMERCE_VERSION='{{ OPENEDX_COMMON_VERSION }}'
RUN mkdir -p /openedx/ecommerce && \
    git clone $ECOMMERCE_REPOSITORY --branch $ECOMMERCE_VERSION --depth 1 /openedx/ecommerce

# Identify tutor user to cherry-pick commits
RUN git config --global user.email "tutor@overhang.io" \
  && git config --global user.name "Tutor"

##### Empty layer with just the repo at the root.
# This is useful when overriding the build context with a host repo:
# docker build --build-context /path/to/ecommerce
FROM scratch as ecommerce-src
COPY --from=checkout /openedx/ecommerce /

###### Install python and virtual environment
FROM minimal as python

RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked{% endif %} \
    apt update && \
    apt install -y libmysqlclient-dev libssl-dev python3 python3-pip python3-venv

ARG APP_USER_ID=1000
RUN if [ "$APP_USER_ID" = 0 ]; then echo "app user may not be root" && false; fi
RUN useradd --home-dir /openedx --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

# Create cache dir. Otherwise, for some reason, it becomes owned by root.
RUN mkdir /openedx/.cache

# Create python venv
RUN python3 -m venv /openedx/venv/
ENV PATH "/openedx/venv/bin:$PATH"
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared,uid=${APP_USER_ID} {% endif %}pip install \
    # https://pypi.org/project/setuptools/
    # https://pypi.org/project/pip/
    # https://pypi.org/project/wheel/
    setuptools==67.7.2 pip==23.1.2. wheel==0.40.0

# Install a recent version of nodejs
# https://pypi.org/project/nodeenv
RUN pip install nodeenv==1.7.0
RUN nodeenv /openedx/nodeenv --node=16.20.0 --prebuilt
ENV PATH /openedx/nodeenv/bin:${PATH}

# Copy ecommerce source code
COPY --from=ecommerce-src --chown=app:app / /openedx/ecommerce
WORKDIR /openedx/ecommerce

# Install npm, bower requirements
ARG NPM_REGISTRY='{{ NPM_REGISTRY }}'
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.npm/,sharing=shared,uid=${APP_USER_ID} {% endif %}npm clean-install --verbose --no-audit --registry=$NPM_REGISTRY
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/bower,sharing=shared,uid=${APP_USER_ID} {% endif %}./node_modules/.bin/bower install --allow-root

# python requirements
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared,uid=${APP_USER_ID} {% endif %}pip install -r requirements.txt
# https://pypi.org/project/uWSGI/
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared,uid=${APP_USER_ID} {% endif %}pip install uwsgi==2.0.21

# Install private requirements: this is useful for installing custom payment processors.
COPY --chown=app:app ./requirements/ /openedx/requirements
RUN cd /openedx/requirements/ \
  && touch ./private.txt \
  && pip install -r ./private.txt

{% for extra_requirement in ECOMMERCE_EXTRA_PIP_REQUIREMENTS %}RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared,uid=${APP_USER_ID} {% endif %}pip install '{{ extra_requirement }}'
{% endfor %}

{{ patch("ecommerce-dockerfile-pre-assets") }}

# Collect static assets (aka: "make static")
COPY --chown=app:app assets.py ./ecommerce/settings/assets.py
ENV DJANGO_SETTINGS_MODULE ecommerce.settings.assets
RUN python3 manage.py update_assets --skip-collect
RUN ./node_modules/.bin/r.js -o build.js
RUN python3 manage.py collectstatic --noinput
RUN python3 manage.py compress --force

# Setup minimal yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV ECOMMERCE_CFG /openedx/config.yml

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
