Ecommerce plugin for `Tutor <https://docs.tutor.overhang.io>`_
===============================================================

This is a plugin for `Tutor <https://docs.tutor.overhang.io>`_ that integrates the `Ecommerce <https://github.com/edx/ecommerce/>`__ application in an Open edX platform.

.. image:: https://overhang.io/static/marketing/img/clients/e-ducation.jpg
    :alt: E-ducation
    :target: https://www.e-ducation.cn/

This plugin was developed and open sourced to the community thanks to the generous support of `E-ducation <https://www.e-ducation.cn/>`_. Thank you!

Installation
------------

This plugin requires tutor>=10.0.0 and the Discovery plugin `tutor-discovery <https://github.com/overhangio/tutor-discovery>`__. If you have installed Tutor by downloading the pre-compiled binary, then both plugins should be automatically installed. You can confirm by running::

    tutor plugins list

But if you have installed tutor from source, then you also need to install the plugin from source::

    pip install tutor-ecommerce

Then, in any case you need to enable the plugins::

    tutor plugins enable discovery ecommerce

Services will have to be re-configured and restarted, so you are probably better off just running quickstart again::

    tutor local quickstart

Note that this plugins is compatible with `Kubernetes integration <http://docs.tutor.overhang.io/k8s.html>`__, so if deploying to a Kubernetes cluster, run instead::

    tutor k8s quickstart

Operations
----------

Creating a user
~~~~~~~~~~~~~~~

The ecommerce user interface will be available at http://ecommerce.local.overhang.io for a local instance, and at ``ECOMMERCE_HOST`` (by  default: ``http(s)://ecommerce.<yours lms host>``) in production. In order to run commands from the UI, a user with admin rights must be created. There are two ways to proceed. To create a brand new user in Ecommerce which will not exist in the LMS, run::

  tutor local run ecommerce ./manage.py createsuperuser

Then login with this new user at: http://ecommerce.local.overhang.io/admin/

To re-use an existing LMS user, first go to http://ecommerce.local.overhang.io/login. You should be redirected to the LMS login page, then to the dashboard. Then this user must be made a staff/superuser in Ecommerce::

    tutor local run ecommerce ./manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.filter(email='USER@EMAIL.COM').update(is_staff=True, is_superuser=True)"

Make sure to replace ``USER@EMAIL.COM`` by the actual user email address. You should then be able to view the Oscar dashboard at http://ecommerce.local.overhang.io.

Configuration
~~~~~~~~~~~~~

- ``ECOMMERCE_HOST`` (default: ``"ecommerce.{{ LMS_HOST }}"``)
- ``ECOMMERCE_PAYMENT_PROCESSORS`` (default: ``{cybersource: {...}, paypal: {...}}`` See below for details.)
- ``ECOMMERCE_ENABLED_PAYMENT_PROCESSORS``: (default: ``["cybersource", "paypal"]``)
- ``ECOMMERCE_ENABLED_CLIENT_SIDE_PAYMENT_PROCESSORS`` (default: ``["cybersource"]``)
- ``ECOMMERCE_EXTRA_PAYMENT_PROCESSOR_CLASSES`` (default: ``[]``)
- ``ECOMMERCE_MYSQL_PASSWORD``: ``"{{ 8|random_string }}"``)
- ``ECOMMERCE_SECRET_KEY`` (default: ``"{{ 20|random_string }}"``)
- ``ECOMMERCE_OAUTH2_SECRET`` (default: ``"{{ 8|random_string }}"``)
- ``ECOMMERCE_API_KEY`` (default: ``"{{ 20|random_string }}"``)
- ``ECOMMERCE_DOCKER_IMAGE`` (default: ``"{{ DOCKER_REGISTRY }}overhangio/openedx-ecommerce:{{ TUTOR_VERSION }}"``)
- ``ECOMMERCE_WORKER_DOCKER_IMAGE`` (default: ``"{{ DOCKER_REGISTRY }}overhangio/openedx-ecommerce-worker:{{ TUTOR_VERSION }}"``)
- ``ECOMMERCE_MYSQL_DATABASE`` (default: ``"ecommerce"``)
- ``ECOMMERCE_MYSQL_USERNAME`` (default: ``"ecommerce"``)
- ``ECOMMERCE_CURRENCY`` (default: ``"USD"``)
- ``ECOMMERCE_OAUTH2_KEY`` (default: ``"ecommerce"``)
- ``ECOMMERCE_API_TIMEOUT`` (default: ``5``)
- ``ECOMMERCE_WORKER_JWT_ISSUER`` (default: ``"ecommerce-worker"``)
- ``ECOMMERCE_EXTRA_PIP_REQUIREMENTS`` (default: ``[]``)

You will need to modify the ``ECOMMERCE_PAYMENT_PROCESSORS`` parameter to configure your payment providers credentials. By default, it is equal to::

  cybersource:
    access_key: SET-ME-PLEASE
    cancel_checkout_path: /checkout/cancel-checkout/
    merchant_id: SET-ME-PLEASE
    payment_page_url: https://testsecureacceptance.cybersource.com/pay
    profile_id: SET-ME-PLEASE
    receipt_page_url: /checkout/receipt/
    secret_key: SET-ME-PLEASE
    send_level_2_3_details: true
    soap_api_url: https://ics2wstest.ic3.com/commerce/1.x/transactionProcessor/CyberSourceTransaction_1.140.wsdl
    sop_access_key: SET-ME-PLEASE
    sop_payment_page_url: https://testsecureacceptance.cybersource.com/silent/pay
    sop_profile_id: SET-ME-PLEASE
    sop_secret_key: SET-ME-PLEASE
    transaction_key: SET-ME-PLEASE
  paypal:
    cancel_checkout_path: /checkout/cancel-checkout/
    client_id: SET-ME-PLEASE
    client_secret: SET-ME-PLEASE
    error_url: /checkout/error/
    mode: sandbox
    receipt_url: /checkout/receipt/

We suggest you modify this configuration, save it to ``ecommerce-config.yml`` and then load it with::

  tutor config save --set "ECOMMERCE_PAYMENT_PROCESSORS=$(cat ecommerce-config.yml)"

Using a custom payment processor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to point to a custom payment processor, named "custompayment", you will first need to add it to the list of enabled payment processors::

    tutor config save --set 'ECOMMERCE_ENABLED_PAYMENT_PROCESSORS=["custompayment"]'

If this is a client-side payment processor, you should also add it to the list of enabled client-side payment processors::

    tutor config save --set 'ECOMMERCE_ENABLED_CLIENT_SIDE_PAYMENT_PROCESSORS=["custompayment"]'

If you need to enable additional ecommerce urls::

    tutor config save --set 'ECOMMERCE_ENABLED_CLIENT_SIDE_PAYMENT_URLS={"custompayment": "ecommerce.extensions.payment.processors.custompayment.urls"}'

Point to the processor class::

    tutor config save --set 'ECOMMERCE_EXTRA_PAYMENT_PROCESSOR_CLASSES=["ecommerce.extensions.payment.processors.custompayment.CustomPayment"]'

Run initialisation scripts to create the right sites and partners::

    tutor local init --limit=ecommerce

Enable the payment processor by creating a waffle switch::

    tutor local run ecommerce ./manage.py waffle_switch --create payment_processor_active_custompayment on

Image customisation
~~~~~~~~~~~~~~~~~~~

Ecommerce implementations vary a lot from one country to another. If all you need are the Paypal, Cybersource and Stripe payment processors, then it should not be necessary to customize the tutor-ecommerce docker image, which contains the vanilla Ecommerce platform. However, if you need to run a fork of Ecommerce, or install extra requirements, then you should re-build the docker image. To do so, first set the appropriate settings::

  tutor config save \
    --set 'ECOMMERCE_EXTRA_PIP_REQUIREMENTS=["git+https://github.com/myusername/myplugin"]'

Then, build the image, pointing to your fork if necessary::

  tutor images build ecommerce \
    -a ECOMMERCE_REPOSITORY=https://github.com/myusername/ecommerce \
    -a ECOMMERCE_VERSION=my/tag

Development
~~~~~~~~~~~

When running Tutor in development mode, the ecommerce service is accessible at http://ecommerce.local.overhang.io:8130.

To mount a local ecommerce repository in the ecommerce container, add the following content to the ``$(tutor config printroot)/env/dev/docker-compose.override.yml`` file::

    version: "3.7"
    services:
      ecommerce:
        volumes:
          - /absolute/path/to/ecommerce:/openedx/ecommerce

You will have to generate static assets in your local repository::

    tutor dev run ecommerce npm install
    tutor dev run ecommerce ./node_modules/.bin/bower install --allow-root
    tutor dev run ecommerce python3 manage.py update_assets --skip-collect

To attach a debugger to the ecommerce service, run::

    tutor dev runserver ecommerce

Implementing a custom payment processor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To work on an extension to ecommerce, it is useful to run Tutor in development mode with hot-reload whenever the source code of dependencies changes. To do so, you should add the source code of your dependency to the requirements folder of the ecommerce Docker image. Then, add your custom dependency in editable mode to the development container image. For instance::

    cd $(tutor config printroot)/env/plugins/ecommerce/build/ecommerce/requirements
    cp -r /path/to/my/custom/myapp ./
    echo "-e ./myapp" >> private.txt

Then, rebuild the ecommerce docker image::

    tutor images build ecommerce

And run the ecommerce service in development mode::

    tutor dev runserver ecommerce

The "myapp" package should be installed inside the Docker image. This can be verified by running::

    tutor dev run ecommerce ./manage.py shell -c "import myapp; print('ok')"

License
-------

This work is licensed under the terms of the `GNU Affero General Public License (AGPL) <https://github.com/overhangio/ecommerce/blob/master/LICENSE.txt>`_.