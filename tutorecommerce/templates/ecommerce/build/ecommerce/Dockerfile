FROM docker.io/ubuntu:20.04

RUN apt update && \
  apt install -y curl git-core language-pack-en libmysqlclient-dev libssl-dev python3 python3-pip python3-venv

# Create python venv
RUN mkdir /openedx/ && python3 -m venv /openedx/venv/
ENV PATH "/openedx/venv/bin:$PATH"
RUN pip install setuptools==44.1.0 pip==20.0.2 wheel==0.34.2

# Install a recent version of nodejs
RUN pip install nodeenv
RUN nodeenv /openedx/nodeenv --node=12.13.0 --prebuilt
ENV PATH /openedx/nodeenv/bin:${PATH}

# Install ecommerce
ARG ECOMMERCE_REPOSITORY=https://github.com/edx/ecommerce.git
ARG ECOMMERCE_VERSION={{ OPENEDX_COMMON_VERSION }}
RUN mkdir -p /openedx/ecommerce && \
    git clone $ECOMMERCE_REPOSITORY --branch $ECOMMERCE_VERSION --depth 1 /openedx/ecommerce
WORKDIR /openedx/ecommerce

# Fix a few issues, and improve custom server-side payment processor extensibility
# https://github.com/edx/ecommerce/pull/3140
# https://github.com/overhangio/ecommerce/commits/overhangio/improve-extensibility
RUN curl https://github.com/overhangio/ecommerce/commit/ba8aaf4b77c8351ea16b69f8b077cfeaab824fc3.patch | git apply -
RUN curl https://github.com/overhangio/ecommerce/commit/e5d5bdc5dc501a85d08d4fd7e534a9b939a16955.patch | git apply -
RUN curl https://github.com/overhangio/ecommerce/commit/e788b836a899f168eeb28a213bddb9d2ca6a44c8.patch | git apply -
RUN curl https://github.com/overhangio/ecommerce/commit/e18da93ad338cfd15b8c53f83c0dd2ee6bcec372.patch | git apply -

# nodejs requirements (aka: "make requirements.js")
ARG NPM_REGISTRY=https://registry.npmjs.org/
RUN npm install --verbose --registry=$NPM_REGISTRY
RUN ./node_modules/.bin/bower install --allow-root

# python requirements
RUN pip install -r requirements.txt
RUN pip install uwsgi==2.0.19.1

# Install private requirements: this is useful for installing custom payment processors.
COPY ./requirements/ /openedx/requirements
RUN cd /openedx/requirements/ \
  && touch ./private.txt \
  && pip install -r ./private.txt

{% for extra_requirement in ECOMMERCE_EXTRA_PIP_REQUIREMENTS %}RUN pip install {{ extra_requirement }}
{% endfor %}

# Collect static assets (aka: "make static")
COPY assets.py ./ecommerce/settings/assets.py
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
