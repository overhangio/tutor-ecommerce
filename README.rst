E-Commerce plugin for `Tutor <https://docs.tutor.overhang.io>`_
===============================================================

This is a plugin for `Tutor <https://docs.tutor.overhang.io>`_ that integrates the `E-Commerce <https://github.com/edx/ecommerce/>`__ application in an Open edX platform.

Installation
------------

This plugin requires tutor>=12.0.0, the `Discovery plugin <https://github.com/overhangio/tutor-discovery>`__ and the `MFE plugin <https://github.com/overhangio/tutor-mfe>`__. If you have installed Tutor by downloading the pre-compiled binary, then both plugins should be automatically installed. You can confirm by running::

    tutor plugins list

But if you have installed tutor from source, then you also need to install the plugin from source::

    pip install tutor-ecommerce

Then, in any case you need to enable the plugins::

    tutor plugins enable discovery ecommerce mfe

Services will have to be re-configured and restarted, so you are probably better off just running quickstart again::

    tutor local quickstart

Note that this plugins is compatible with `Kubernetes integration <http://docs.tutor.overhang.io/k8s.html>`__. When deploying to a Kubernetes cluster, run instead::

    tutor k8s quickstart

For further instructions on how to setup E-Commerce with Open edX, check the `official E-Commerce documentation <https://edx-ecommerce.readthedocs.io/en/latest/>`__.

Configuration
-------------

- ``ECOMMERCE_HOST`` (default: ``"ecommerce.{{ LMS_HOST }}"``)
- ``ECOMMERCE_PAYMENT_PROCESSORS`` (default: ``{cybersource: {...}, paypal: {...}}`` See below for details.)
- ``ECOMMERCE_ENABLE_IDENTITY_VERIFICATION``: (default: ``True``)
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
        merchant_id: SET-ME-PLEASE 
        flex_shared_secret_key_id: SET-ME-PLEASE
        flex_shared_secret_key: SET-ME-PLEASE
        soap_api_url: https://ics2wstest.ic3.com/commerce/1.x/transactionProcessor/CyberSourceTransaction_1.140.wsdl
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

Cybersource
~~~~~~~~~~~

To enable the `Cybersource <https://cybersource.com>`__ payment processor, two keys need to be generated. In your Cybersource account, go to "Payment Configuration" 🠆 "Key Management" 🠆 "Generate key". Create the following keys: 

- SOAP API key: use this key to define the ``transaction_key`` setting.
- REST Shared secret: use the key ID and value to define ``flex_shared_secret_key_id`` and ``flex_shared_secret_key``, respectively.

The ``merchant_id`` setting corresponds to your Merchant ID.

Operations
----------

Creating a user
~~~~~~~~~~~~~~~

The ecommerce user interface will be available at http://ecommerce.local.overhang.io for a local instance, and at ``ECOMMERCE_HOST`` (by  default: ``http(s)://ecommerce.<yours lms host>``) in production. In order to run commands from the UI, a user with admin rights must be created. There are two ways to proceed. To create a brand new user in E-Commerce which will not exist in the LMS, run::

  tutor local run ecommerce ./manage.py createsuperuser

Then login with this new user at: http://ecommerce.local.overhang.io/admin/

To re-use an existing LMS user, first go to http://ecommerce.local.overhang.io/login. You should be redirected to the LMS login page, then to the dashboard. Then this user must be made a staff/superuser in E-Commerce::

    tutor local run ecommerce ./manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.filter(email='USER@EMAIL.COM').update(is_staff=True, is_superuser=True)"

Make sure to replace ``USER@EMAIL.COM`` by the actual user email address. You should then be able to view the Oscar dashboard at http://ecommerce.local.overhang.io.


Custom payment processors
~~~~~~~~~~~~~~~~~~~~~~~~~

⚠️ WARNING: as of Lilac (Tutor v12), Open edX no longer supports custom payment processors with E-Commerce. There is an ongoing conversation about how to resolve this issue which you can follow `here <https://discuss.openedx.org/t/urgent-ecommerce-in-lilac-custom-payment-processors-broken/5055>`__.

Image customisation
~~~~~~~~~~~~~~~~~~~

E-Commerce implementations vary a lot from one country to another. If all you need are the Paypal, Cybersource and Stripe payment processors, then it should not be necessary to customize the tutor-ecommerce docker image, which contains the vanilla E-Commerce platform. However, if you need to run a fork of E-Commerce, or install extra requirements, then you should re-build the docker image. To do so, first set the appropriate settings::

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

Funding
-------

.. image:: https://overhang.io/static/marketing/img/clients/e-ducation.jpg
    :alt: E-ducation
    :target: https://www.e-ducation.cn/

This plugin was developed and open sourced to the community thanks to the generous support of `E-ducation <https://www.e-ducation.cn/>`_. Thank you!

License
-------

This work is licensed under the terms of the `GNU Affero General Public License (AGPL) <https://github.com/overhangio/ecommerce/blob/master/LICENSE.txt>`_.
