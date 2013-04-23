"""In Django terms, :mod:`itt.control.test` is an app that presents a URI
endpoint for ITT node instances to commit test checkpoints.

The URI endpoint is defined as follows::

    http://<hostname>:8080/test/checkpoint/

.. note::

    TODO: Authenticate node access to the resource (US23)

The URI endpoint is RESTful in nature and follows the principles
behind HTTP POST methods to create a resource on the server.

.. note::

    In terms of a REST-style architecture, a "resource" is a
    collection of similar data.  In this case, the data refers to
    ITT test checkpoints.

    The ITT RESTful interface is built on top of :mod:`tastypie`.
    Tastypie is a webservice API framework for Django.  More
    information can be found at
    http://django-tastypie.readthedocs.org/en/v0.9.12/index.html

The following example demonstrates the simplest form of a checkpoint commit
using the :mod:`requests` module:

    >>> import requests, json
    >>> payload = {'data': 'payload'}
    >>> url = 'http://127.0.0.1:8080/test/checkpoint/'
    >>> headers = {'content-type': 'application/json'}
    >>> r = requests.post(url,
    ...                   data=json.dumps(payload),
    ...                   headers=headers)

The default behaviour of the POST method instance is to return a
serialized form of the data.  This can be obtained via the `text`
attribute of the `Response` object `r`:

    >>> r.text
    u'{"data": "payload", "date": "2013-04-22T12:37:44.835514", ...}'

.. note::

    Any modifications to the ITT Control and Command models will require
    a fresh database initialisation to build the appropriate structure.
    This can be done with the ``Makefile`` under the ``init`` target::

    $ make init

"""
