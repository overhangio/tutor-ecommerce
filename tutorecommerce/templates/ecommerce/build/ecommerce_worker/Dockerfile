FROM docker.io/ubuntu:18.04

RUN apt update && \
  apt install -y git-core language-pack-en python python-pip python-virtualenv

RUN mkdir -p /openedx/ecommerce_worker && \
    git clone https://github.com/edx/ecommerce-worker.git --branch open-release/ironwood.2 --depth 1 /openedx/ecommerce_worker
WORKDIR /openedx/ecommerce_worker

# Install python venv
RUN virtualenv ../venv/
ENV PATH "/openedx/venv/bin:$PATH"
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements/production.txt

ENV WORKER_CONFIGURATION_MODULE ecommerce_worker.settings.production
CMD celery worker --app=ecommerce_worker.celery_app:app --loglevel=info  --maxtasksperchild 100 --queue=fulfillment,email_marketing
