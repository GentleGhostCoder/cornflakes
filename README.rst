cornflakes
==========

|PyPI| |Python Version| |License| |Read the Docs| |Build| |Tests| |Codecov|

.. |PyPI| image:: https://img.shields.io/pypi/v/cornflakes.svg
   :target: https://pypi.org/project/cornflakes/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/cornflakes
   :target: https://pypi.org/project/cornflakes
   :alt: Python Version
.. |License| image:: https://img.shields.io/github/license/semmjon/cornflakes
   :target: https://opensource.org/licenses/Apache2.0
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/cornflakes/latest.svg?label=Read%20the%20Docs
   :target: https://cornflakes.readthedocs.io
   :alt: Read the documentation at https://cornflakes.readthedocs.io
.. |Build| image:: https://github.com/semmjon/cornflakes/workflows/Build%20cornflakes%20Package/badge.svg
   :target: https://github.com/semmjon/cornflakes/actions?workflow=Package
   :alt: Build Package Status
.. |Tests| image:: https://github.com/semmjon/cornflakes/workflows/Run%20cornflakes%20Tests/badge.svg
   :target: https://github.com/semmjon/cornflakes/actions?workflow=Tests
   :alt: Run Tests Status
.. |Codecov| image:: https://codecov.io/gh/semmjon/cornflakes/branch/release-1.4.5/graph/badge.svg?token=FY72EIXI82
   :target: https://codecov.io/gh/semmjon/cornflakes
   :alt: Codecov

.. code::

   pip install cornflakes

Information
-----------

This package was created by starting C ++ methods to incorporate into my python implementations.
To make things easier for me, lightweight public libraries were included
(especially to carry out string operations):

* hash-library
* strtk

Features:
~~~~~~~~~

The following features have currently been implemented:
    * config management system
        - based on dataclass
        - alternative Implementation for pydantic (BaseSettings)
        - ini support files by a lightweight and fast parser (-> ini_load)
        - yaml support (based on PyYAML)
        - environment variables
        - (future) support json (based on orjson)
    * command line interface management
        - method: click_cli (decorator)
        - based on click and rich
        - easy to use and start with
    * eval_type
        - method to parse strings in python-types e.g. int | bool | timestamp
    * simple_hmac
        - vectorized c++ hmac implementation
    * default_ca_path
        - python function to find a default ssl / ca certificate path

Currently, the package is tested for Linux, Mac and Windows

Development
-----------

Prerequisites
~~~~~~~~~~~~~

-  A compiler with C++17 support
-  Pip 10+ or CMake >= 3.4 (or 3.8+ on Windows, which was the first version to support VS 2015)
-  Python 3.8+

Commands
~~~~~~~~~~~~

Just clone this repository and pip install. Note the ``--recursive``
option which is needed for the pybind11 submodule:

.. code::

   git clone --recursive https://gitlab.blubblub.tech/sgeist/cornflakes.git

Install the package using makefiles:

.. code::

   make install

Build dist using makefiles:

.. code::

   make dist

Run tests (pytest) using makefiles:

.. code::

   make test


Run all tests using makefiles:

.. code::

   make test-all

Run lint using makefiles:

.. code::

   make lint

Create dev venv:

.. code::

   python -m venv .venv
   source .venv/bin/activate
   pip install cookietemple ninja pre-commit poetry

Bump Version using cookietemple:

.. code::

   cookietemple bump-version "<version(e.g 0.0.1)>"

Run lint using cookietemple:

.. code::

   cookietemple lint .

Install pre-commit:

.. code::

   pre-commit install

Update pre-commit:

.. code::

   pre-commit update -a

Run pre-commit:

.. code::

   pre-commit run -a

Publish
~~~~~~~

Its not recommended publish manually (use git-ci or github workflows instead).

.. code::

   make publish
