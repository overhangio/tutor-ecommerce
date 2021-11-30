FROM docker.io/ubuntu:20.04

RUN apt update && \
  apt install -y curl git-core language-pack-en libmysqlclient-dev libssl-dev python3 python3-pip python3-venv

ARG APP_USER_ID=1000
RUN useradd --home-dir /openedx --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

# Create python venv
RUN python3 -m venv /openedx/venv/
ENV PATH "/openedx/venv/bin:$PATH"
RUN pip install setuptools==44.1.0 pip==20.3.4 wheel==0.37.0

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

# Identify tutor user to cherry-pick commits
RUN git config --global user.email "tutor@overhang.io" \
  && git config --global user.name "Tutor"

# Fix payment MFE connection
# https://github.com/edx/ecommerce/pull/3586
RUN git fetch https://github.com/bloomedn/ecommerce 3f9af6ac48b26b579419fcdec2efb06aecc961eb && git cherry-pick 3f9af6ac48b26b579419fcdec2efb06aecc961eb
RUN git fetch https://github.com/bloomedn/ecommerce 5fcb85218a5f4b1d4bd413a40f0a40801685bece && git cherry-pick 5fcb85218a5f4b1d4bd413a40f0a40801685bece

# nodejs requirements (aka: "make requirements.js")
ARG NPM_REGISTRY=https://registry.npmjs.org/
RUN npm install --verbose --registry=$NPM_REGISTRY
RUN ./node_modules/.bin/bower install --allow-root

# python requirements
RUN pip install -r requirements.txt
RUN pip install uwsgi==2.0.19.1

# Install private requirements: this is useful for installing custom payment processors.
COPY --chown=app:app ./requirements/ /openedx/requirements
RUN cd /openedx/requirements/ \
  && touch ./private.txt \
  && pip install -r ./private.txt

{% for extra_requirement in ECOMMERCE_EXTRA_PIP_REQUIREMENTS %}RUN pip install {{ extra_requirement }}
{% endfor %}

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
