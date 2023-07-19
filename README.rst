.. image:: https://github.com/semmjon/cornflakes/blob/main/assets/cornflakes.png?raw=true
   :height: 400 px
   :width: 400 px
   :alt: cornflakes logo
   :align: center

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
.. |Codecov| image:: https://codecov.io/gh/semmjon/cornflakes/branch/release-1.4.5/graph/badge.svg
   :target: https://codecov.io/gh/semmjon/cornflakes
   :alt: Codecov
.. |Pre-Commit-CI| image:: https://results.pre-commit.ci/badge/github/sgeist-ionos/cornflakes/main.svg
   :target: https://results.pre-commit.ci/latest/github/sgeist-ionos/cornflakes/main
   :alt: pre-commit.ci status

.. code::

   pip install cornflakes

.. code::

    pip install git+https://github.com/semmjon/cornflakes

.. warning::
    Please be careful when using this Python module. Currently it is only developed / tested by me, which is why it has a high update / change rate. I'm actually trying to be compatible with implementations, but I can't guarantee this at the moment. The module is currently still in a beta state and is not recommended for productive use.

    In the near future I plan to revise the documentation / examples and write an introductory blog article, as I find implemented features and planned ideas to be quite cool and useful (and don't see them in any other package or find them to be quite user-friendly).

Information
-----------

The Python module "cornflakes" was started as a hobby project and offers an alternative to Pydantic for managing configurations and data structures. It allows creating generic and easy to manage configurations for your project. Unlike Pydantic, which is based on inheritance, "cornflakes" uses a decorator (similar to dataclass) to map data structures.

In addition to a dataclass decorator with additional functionality, there is also a config decorator. This makes it possible to read the dataclass from configuration files. This can be very useful if you want to save your application configurations to a file.

The module also has a click wrapper that simplifies the implementation of command line applications. By integrating the Rich module, the application is additionally equipped with colors and other functions.

There are other useful methods in the base of the module that are generally useful for Python development. These can help you develop your projects faster and more efficiently.

Short Term RoadMap:
~~~~~~~~~~~~~~~~~~~~

- Change Code Annotations
    - remove Any annotations if possible
    - change Protocol Annotations to specific type classes
- Enrich json methods
- Fix / Test the to_<file-format> Methods (specially yaml)

Development
-----------

Prerequisites
~~~~~~~~~~~~~

-  A compiler with C++17 support
-  Pip 10+ or CMake >= 3.4 (or 3.8+ on Windows, which was the first version to support VS 2015)
-  Python 3.8+
-  doxygen
-  cppcheck
-  clang-tools-extra or clang-tidy
-  ..

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
   pip install ninja pre-commit poetry

Install pre-commit:

.. code::

   pre-commit install

Update pre-commit:

.. code::

   pre-commit update -a

Run pre-commit:

.. code::

   pre-commit run -a
