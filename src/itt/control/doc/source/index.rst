.. ITT Control and Command documentation master file

.. toctree::
   :maxdepth: 2

IP Test Control and Command
===========================

.. note::
    The Control and Command is somewhat of a WIP so it's exact
    usage is still evolving.  As new functionality is defined, place a
    reference within this file.

The IP Test Tool Control and Command primary role is to act as a mediator
between the various ITT components.

Built within the Django framework, the Control and Command is a web-based
system featuring a series of individual apps.  Each app is itself a Python
package.

General Notes Around Testing
----------------------------
The tests have been moved from the "preferred" Django location and into
``<project>/<app>/tests/test_<name>.py`` file to be more consistent with
the ITT project.  Of course, the Django test runner does not like this.
However, problem can be resolved by making an import call within
__init__.py.  For example, if I have a test called
``<project>/<app>/tests/test_x.py``, place the following line into
``<project>/<app>/tests/__init__.py``::

    from test_x import <test_class>

With this construct, you can target individual test classes or test
methods as follows:

**Test classes**::

    $ ./manage.py test <app>.<test_class>

**Test class methods**::

    $ ./manage.py test <app>.<test_class>.<test_class_method>

Running the Test Instance of the Django ITT Project
---------------------------------------------------
Standard Django stuff here -- much more information can be found at
https://docs.djangoproject.com/en/dev/topics/testing/overview/#running-tests

In brief, the test suite can be launched with the ``manage.py`` utility
which can be found in the ITT Control and Command project root directory.  
Also the ``Makefile`` provides a wrapper around this utility in addition to 
preparint the environment for you::

  $ make test

:mod:`itt.control.common` - Common ITT Django Functionality
-----------------------------------------------------------

.. automodule:: itt.control.common.models

:mod:`itt.control.common.models` - methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: itt.control.common.models.CommonModel.get_fields

:mod:`itt.control.test` -- Modules
----------------------------------

.. automodule:: itt.control.test

:mod:`itt.control.test_checkpoint.api` -- The ITT Test Case RESTful API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: itt.control.test_checkpoint.api
    :members:
    :show-inheritance:

:mod:`itt.control.test_checkpoint.models` -- The ITT Test Case Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: itt.control.test_checkpoint.models
   :members:
   :show-inheritance:

:mod:`itt.control.test_checkpoint.views` -- The ITT Test Case Views
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: itt.control.test_checkpoint.views
   :members:
   :show-inheritance:

:mod:`itt.control.server` -- Modules
------------------------------------

 .. automodule:: itt.control.server

:mod:`itt.control.server.views` -- The ITT Server View
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: itt.control.server.views
    :members:
    :show-inheritance:

:mod:`itt.control.server.models` -- The ITT Server Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: itt.control.server.models
   :members:
   :show-inheritance:

:mod:`itt.control.config` -- Modules
------------------------------------

 .. automodule:: itt.control.config

:mod:`itt.control.config.views` -- The ITT Config View
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: itt.control.config.views
    :members:
    :show-inheritance:

:mod:`itt.control.config.models` -- The ITT Config Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: itt.control.config.models
   :members:
   :show-inheritance:

:mod:`itt.control.test_config` -- Modules
-----------------------------------------

 .. automodule:: itt.control.test_config

:mod:`itt.control.test_config.views` -- The ITT Test Config View
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: itt.control.test_config.views
    :members:
    :show-inheritance:

:mod:`itt.control.test_config.models` -- The ITT Test Config Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: itt.control.test_config.models
   :members:
   :show-inheritance:

:mod:`itt.control.test_content` -- Modules
------------------------------------------

 .. automodule:: itt.control.test_content

:mod:`itt.control.test_content.views` -- The ITT Test Content View
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: itt.control.test_content.views
    :members:
    :show-inheritance:

:mod:`itt.control.test_content.models` -- The ITT Test Content Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: itt.control.test_content.models
   :members:
   :show-inheritance:

:mod:`itt.control.test_connection` -- Modules
---------------------------------------------

 .. automodule:: itt.control.test_connection

:mod:`itt.control.test_connection.views` -- The ITT Test Connection View
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: itt.control.test_connection.views
    :members:
    :show-inheritance:

:mod:`itt.control.test_connection.models` -- The ITT Test Connection Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: itt.control.test_connection.models
   :members:
   :show-inheritance:

:mod:`itt.control.test_case` -- Modules
---------------------------------------

 .. automodule:: itt.control.test_case

:mod:`itt.control.test_case.views` -- The ITT Test Case View
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: itt.control.test_case.views
    :members:
    :show-inheritance:

:mod:`itt.control.test_case.models` -- The ITT Test Case Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: itt.control.test_case.models
   :members:
   :show-inheritance:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
