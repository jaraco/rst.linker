.. image:: https://img.shields.io/pypi/v/rst.linker.svg
   :target: https://pypi.org/project/rst.linker

.. image:: https://img.shields.io/pypi/pyversions/rst.linker.svg

.. image:: https://img.shields.io/pypi/dm/rst.linker.svg

.. image:: https://img.shields.io/travis/jaraco/rst.linker/master.svg
   :target: http://travis-ci.org/jaraco/rst.linker

``rst.linker`` provides a routine for adding links and performing
other custom replacements to reStructuredText files as a Sphinx
extension.

License
=======

License is indicated in the project metadata (typically one or more
of the Trove classifiers). For more details, see `this explanation
<https://github.com/jaraco/skeleton/issues/1>`_.

Usage
=====

In your sphinx ``conf`` file, include ``rst.linker`` as an extension
and then add a ``link_files`` configuration section describing
the substitutions to make. For an example, see `rst.linker's own
conf.py
<https://github.com/jaraco/rst.linker/blob/master/docs/conf.py>`_
or read the source to learn more about the the linkers provided.
