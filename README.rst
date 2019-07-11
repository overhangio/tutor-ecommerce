Ecommerce plugin for `Tutor <https://docs.tutor.overhang.io>`_
===============================================================

This is a plugin for `Tutor <https://docs.tutor.overhang.io>`_ that integrates the `Ecommerce <https://github.com/edx/ecommerce/>`__ application in an Open edX platform.

.. image:: https://overhang.io/images/clients/e-ducation.jpg
    :alt: E-ducation
    :target: https://www.e-ducation.cn/

This plugin was developed and open sourced to the community thanks to the generous support of `E-ducation <https://www.e-ducation.cn/>`_. Thank you!

Installation
------------

This plugin requires tutor>=3.6.0 and the Discovery plugin `tutor-discovery <https://github.com/overhangio/tutor-discovery>`__. Also, you should have installed tutor from source, and not from a pre-compiled binary.

::

    pip install tutor-ecommerce

Then, to enable this plugin, run::

    tutor plugins enable ecommerce

Services will have to be re-configured and restarted, so you are probably better off just running quickstart again::

    tutor local quickstart

Note that this plugins is compatible with `Kubernetes integration <http://docs.tutor.overhang.io/k8s.html>`__, so if deploying to a Kubernetes cluster, run instead::

    tutor k8s quickstart

Operations
----------

Creating a user
~~~~~~~~~~~~~~~

The ecommerce user interface will be available at http://ecommerce.localhost for a local instance, and at ``ECOMMERCE_HOST`` (by  default: ``http(s)://ecommerce.<yours lms host>``) in production. In order to run commands from the UI, a user with admin rights must be created::

  tutor local run ecommerce ./manage.py createsuperuser

Local development
~~~~~~~~~~~~~~~~~

For developing locally, it is necessary to configure the ecommerce service to be served from localhost::

  tutor config save --set ECOMMERCE_HOST=ecommerce.localhost

Configuration
~~~~~~~~~~~~~

- ``ECOMMERCE_HOST`` (default: ``"ecommerce.{{ LMS_HOST }}"``)
- ``ECOMMERCE_PAYMENT_PROCESSORS`` (default: ``{cybersource: {}, paypal: {}}``)
- ``ECOMMERCE_ENABLED_PAYMENT_PROCESSORS``: (default: ``["cybersource", "paypal"]``)
- ``ECOMMERCE_ENABLED_CLIENT_SIDE_PAYMENT_PROCESSORS`` (default: ``["cybersource"]``)
- ``ECOMMERCE_EXTRA_PAYMENT_PROCESSOR_CLASSES`` (default: ``[]``)
- ``ECOMMERCE_MYSQL_PASSWORD``: ``"{{ 8|random_string }}"``)
- ``ECOMMERCE_SECRET_KEY`` (default: ``"{{ 20|random_string }}"``)
- ``ECOMMERCE_OAUTH2_SECRET`` (default: ``"{{ 8|random_string }}"``)
- ``ECOMMERCE_API_KEY`` (default: ``"{{ 20|random_string }}"``)
- ``ECOMMERCE_DOCKER_IMAGE`` (default: ``"overhangio/openedx-ecommerce:{{ TUTOR_VERSION }}"``)
- ``ECOMMERCE_WORKER_DOCKER_IMAGE`` (default: ``"overhangio/openedx-ecommerce-worker:{{ TUTOR_VERSION }}"``)
- ``ECOMMERCE_MYSQL_DATABASE`` (default: ``"ecommerce"``)
- ``ECOMMERCE_MYSQL_USERNAME`` (default: ``"ecommerce"``)
- ``ECOMMERCE_MYSQL_USERNAME`` (default: ``"ecommerce"``)
- ``ECOMMERCE_OAUTH2_KEY`` (default: ``"ecommerce"``)
- ``ECOMMERCE_API_TIMEOUT`` (default: ``5``)
- ``ECOMMERCE_WORKER_JWT_ISSUER`` (default: ``"ecommerce_worker"``)
- ``ECOMMERCE_EXTRA_PIP_REQUIREMENTS`` (default: ``[]``)

Image customisation
~~~~~~~~~~~~~~~~~~~

Ecommerce implementations vary a lot from one country to another. If all you need are the Paypal, Cybersource and Stripe payment processors, then it should not be necessary to customize the tutor-ecommerce docker image, which contains the vanilla Ecommerce platform. However, if you need to run a fork of Ecommerce, or install extra requirements, then you should re-build the docker image. To do so, first set the appropriate settings::

  tutor config save \
    --set 'ENABLED_PAYMENT_PROCESSORS=["myprocessor"]' \
    --set 'ENABLED_CLIENT_SIDE_PAYMENT_PROCESSORS=["myprocessor"]' \
    --set 'ECOMMERCE_EXTRA_PAYMENT_PROCESSOR_CLASSES=["myextension.payment.MyProcessor"]' \
    --set 'ECOMMERCE_EXTRA_PIP_REQUIREMENTS=["git+https://github.com/myusername/myplugin"]'

Then, build the image, pointing to your fork if necessary::

  tutor images build ecommerce \
    -a ECOMMERCE_REPOSITORY=https://github.com/myusername/ecommerce \
    -a ECOMMERCE_VERSION=my/tag
