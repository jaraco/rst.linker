v2.3.0
======

#9: Fixed syntax errors in docs.

Require Python 3.7 or later.

v2.2.0
======

#8: Prefer author date to committer date when adding SCM
timestamps, reverting change in 2.1, and this time tracking
the motivation more carefully.

v2.1.1
======

Fix Github Actions badge.

v2.1.0
======

Prefer committer date to author date when adding SCM
timestamps.

v2.0.0
======

Drop support for Python 3.5 and earlier.

1.11
====

Now supply the version of the package during Sphinx
setup.

Also supply "parallel_read_safe=True" to be explicit
about the suspicion that this plugin is safe for
parallel reads.

1.10
====

Refreshed package metadata.

Package now presents the ``rst`` package a pkg-util
namespace package (instead of pkg_resources).

1.9
===

Replacer now adds the Sphinx config namespace to the
replacements, meaning that names like ``project``
or ``copyright`` may be referenced in the format
strings. This feature is particularly useful when
coupled with the `jaraco.packaging
<https://pypi.org/project/jaraco.packaging>`_.sphinx
plugin, which supplies a ``package_url``.

1.8.2
=====

Added project description and updated changelog.

1.8.1
=====

Issue #4: Prefer public API of ``app.confdir`` to private
API.

1.8
===

Issue #4: Resolve deterministically the filenames relative to
the config file.

*semver deviation*: This change is backward-incompatible
for projects that relied on paths relative to the cwd where
the cwd was not the directory of the config file.

1.7
===

Issue #2: Suppress stderr from SCM programs.

1.6.2
=====

Issue #3: Fix incorrect call on open call to write the linked
target.

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
