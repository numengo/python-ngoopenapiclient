========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-ngoopenapiclient/badge/?style=flat
    :target: https://readthedocs.org/projects/python-ngoopenapiclient
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/romancedric/python-ngoopenapiclient.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/romancedric/python-ngoopenapiclient

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/romancedric/python-ngoopenapiclient?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/romancedric/python-ngoopenapiclient

.. |requires| image:: https://requires.io/github/romancedric/python-ngoopenapiclient/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/romancedric/python-ngoopenapiclient/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/romancedric/python-ngoopenapiclient/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/romancedric/python-ngoopenapiclient

.. |version| image:: https://img.shields.io/pypi/v/ngoopenapiclient.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/ngoopenapiclient

.. |commits-since| image:: https://img.shields.io/github/commits-since/romancedric/python-ngoopenapiclient/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/romancedric/python-ngoopenapiclient/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/ngoopenapiclient.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/ngoopenapiclient

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/ngoopenapiclient.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/ngoopenapiclient

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/ngoopenapiclient.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/ngoopenapiclient


.. end-badges

API client for API serving a swagger/openAPI schema

* Free software: GNU General Public License v3

.. skip-next

Installation
============

Install command::

    pip install ngoopenapiclient

Documentation
=============

https://python-ngoopenapiclient.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
