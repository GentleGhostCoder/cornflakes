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

This package was created by starting C ++ methods to incorporate into my
python implementations.

To make things easier for me, lightweight public libraries were included
(especially to carry out string operations):

* hash-library
* strtk

The following methods have currently been implemented:

* ini_load (flexible and ligthweigh ini to dict parser, Faster Than Configparser)
* eval_type (method to parse strings in python-types e.g. int \| bool \| timestamp
* simple_hmac (vectorized c++ hmac implementation)
* default_ca_path (python function to find a default ssl / ca certificate path)

In the future the following will be implemented: - more hash methods -
c++ optimized grep methods - c++ optimized url-tools methods

Currently, the package was only tested for Linux ## Usage

.. code:: python

   from cornflakes import ini_load, default_ca_path, eval_type

   ini_load(files={"s3_configs": ["examples/config/aws_config",
                                  "examples/config/aws_credentials",
                                  "examples/config/.s3cfg"]},
            sections=["default", "qa"],
            keys={"signurl_use_https": ["signurl_use_https"],
                  "aws_access_key_id": ["access_key"],
                  "aws_secret_access_key": ["secret_key"],
                  "endpoint_url": ["endpoint-url", "host_base"],
                  "region_name": ["bucket_location", "region", "aws_default_region"],
                  "service_name": ["service_name"],
                  "verify": ["ca_certs", "aws_ca_bundle", "ca_bundle"],},
            defaults={
                "region_name": "us-east-1",
                "signurl_use_https": True,
                "verify": default_ca_path(),
                "service_name": "s3",
            })

Development
-----------

Prerequisites
~~~~~~~~~~~~~

-  A compiler with C++17 support
-  Pip 10+ or CMake >= 3.4 (or 3.8+ on Windows, which was the first
   version to support VS 2015)
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
