.. image:: https://img.shields.io/pypi/v/rst.linker.svg
   :target: https://pypi.org/project/rst.linker

.. image:: https://img.shields.io/pypi/pyversions/rst.linker.svg

.. image:: https://github.com/jaraco/rst.linker/actions/workflows/main.yml/badge.svg
   :target: https://github.com/jaraco/rst.linker/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. image:: https://readthedocs.org/projects/rstlinker/badge/?version=latest
   :target: https://rstlinker.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/skeleton-2025-informational
   :target: https://blog.jaraco.com/skeleton


``rst.linker`` provides a routine for adding links and performing
other custom replacements to reStructuredText files as a Sphinx
extension.

Usage
=====

In your sphinx ``conf`` file, include ``rst.linker`` as an extension
and then add a ``link_files`` configuration section describing
the substitutions to make. For an example, see `rst.linker's own
conf.py
<https://github.com/jaraco/rst.linker/blob/master/docs/conf.py>`_
or read the source to learn more about the the linkers provided.
