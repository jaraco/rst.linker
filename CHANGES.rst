1.6.1
=====

Explicitly specify that source file must be encoded in UTF-8
to support encoding on systems where LANG=C.

1.6
===

Automated deployments via Travis-CI.

Issue #1: Tests now xfail when no Git repository is available.

1.5
===

``timestamp`` in SCM info is now parsed into a
timezone-aware datetime.datetime object, allowing
for the timezone to be rendered using arbitrary
date formatting.

1.4.2
=====

Fix Replacer resolution on Python 2.

1.4
===

Refined implementation and example for linking timestamps.
Added support for Mercurial repos.

1.3.1
=====

Fix error on Python 2 due to old-style class resolution.

1.3
===

Moved hosting to Github.

Add support for linking timestamps from a git repository according to
version tags as found in the file.

Use setuptools_scm again.

1.1
===

Use hgtools due to setuptools_scm #21.

1.0
===

Initial release.
