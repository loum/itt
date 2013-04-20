.. ITT Control and Command documentation master file

IP Test Control and Command
===========================

.. note:: The Control and Command is somewhat of a WIP so it's exact
    usage is still evolving.  As new functionality is defined, place a
    reference within this file.

The IP Test Tool Control and Command primary role is to act as a mediator
between the various ITT components.

The Control and Command is a web-based application built on top of the
Django framework

.. toctree::
   :maxdepth: 2

Modules
-------

:mod:`itt.control.test.api` -- The ITT Test Case RESTful API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: test.api
    :members:
    :show-inheritance:

:mod:`itt.control.test.models` -- The ITT Test Case Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: test.models
   :members:
   :show-inheritance:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
