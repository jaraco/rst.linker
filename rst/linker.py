"""
Sphinx plugin to add links and timestamps to the changelog.
"""

import functools
import operator
import os
import re
from collections.abc import Mapping
from importlib import metadata

import jaraco.vcs as vcs
from jaraco.context import suppress


class Repl:
    @classmethod
    def from_defn(cls, defn):
        "Return the first Repl subclass that works with this"
        instances = (subcl(defn) for subcl in cls.__subclasses__())
        return next(filter(None, instances))

    def __init__(self, defn):
        vars(self).update(defn)

    def matches(self, text):
        return re.match(self.pattern + '$', text)

    def __bool__(self):
        return False


class URLLinker(Repl):
    r"""
    Each replacement should have the form::

        {
            pattern: "Issue #?(?P<number>\d+)",
            url: "{bitbucket}/jaraco/rst.linker/issues/{number}",
            bitbucket: https://bitbucket.org
        }

    Currently, each named group must be unique across all Repl objects used
    in a replacement.
    """

    def replace(self, match, replacer_vars):
        text = match.group(0)
        ns = match.groupdict()
        ns.update(vars(self))
        ns.update(replacer_vars)
        hyperlink = '`{text} <{href}>`_'
        return hyperlink.format(text=text, href=self.url.format(**ns))

    def __bool__(self):
        return 'url' in vars(self)


class SCMTimestamp(Repl):
    r"""
    Replace content with a version number to include the date stamp
    from the SCM.

    For example, consider a changelog with the following::

        1.0
        ---

        Changed something.

    The following replacement definition would add a datestamp
    after the heading::

        {
            pattern: r"(?m:^((?P<scm_version>\d+(\.\d+){1,2})\n-+\n))",
            with_scm: "{text}\nTagged {rev[timestamp]}\n",
        }

    If the scm_version is detected, a timestamp will be added to the
    namespace.

    If detected, the rev[timestamp] is a datetime-aware timestamp,
    so arbitrary formatting operators may be applied to it, such as
    the following which will render as "Dec 2000"::

        {
            with_scm: "{rev[timestamp]:%b %Y}",
        }
    """

    def replace(self, match, replacer_vars):
        text = match.group(0)
        scm_version = match.group('scm_version')
        rev = self._get_scm_info_for(scm_version)
        if not rev:
            return text
        ns = match.groupdict()
        ns.update(vars(self))
        ns.update(replacer_vars)
        return self.with_scm.format(text=text, rev=rev, **ns)

    @staticmethod
    @suppress(Exception)
    def _get_scm_info_for(scm_version):
        return dict(timestamp=vcs.repo().get_timestamp(scm_version))

    def __bool__(self):
        return 'with_scm' in vars(self)


class Replacer(list):
    @staticmethod
    def load(filename):
        defn = dict()
        with open(filename) as stream:
            exec(stream.read(), defn)
        return defn

    @classmethod
    def from_definition(cls, defn, names: Mapping = {}):
        """
        A definition may contain the following members:

        - using: a dictionary of variables available for substitution
        - replace: a list of replacement definitions.
        """
        repls = map(Repl.from_defn, defn.get('replace', []))
        self = cls(repls)
        vars(self).update(names)
        vars(self).update(defn.get('using', {}))
        return self

    def run(self, source):
        by_pattern = operator.attrgetter('pattern')
        pattern = '|'.join(map(by_pattern, self))
        return re.sub(pattern, self.replace, source)

    def replace(self, match):
        text = match.group(0)
        # determine which replacement matched
        repl = next(repl for repl in self if repl.matches(text))
        return repl.replace(match, vars(self))

    def write_links(self, source, target):
        with open(source, encoding='utf-8') as source:
            out = self.run(source.read())
        with open(target, 'w', encoding='utf-8') as dest:
            dest.write(out)


def setup(app):
    app.add_config_value('link_files', {}, '')
    app.connect('builder-inited', make_links)
    return dict(version=metadata.version('rst.linker'), parallel_read_safe=True)


def _extend_name(filename):
    base, ext = os.path.splitext(filename)
    return base + ' (links)' + ext


def _locater(app):
    """
    Return a function suitable for locating the path
    relative to the config container.
    """
    return functools.partial(os.path.join, app.confdir)


def config_dict(config):
    """
    Given a Sphinx config object, return a dictionary of config
    values.
    """
    return dict((key, getattr(config, key)) for key in config.values)


def make_links(app):
    files_def = app.config.link_files
    _locate = _locater(app)
    for filename, defn in files_def.items():
        source = _locate(filename)
        replacer = Replacer.from_definition(defn, config_dict(app.config))
        target = _extend_name(source)
        replacer.write_links(source, target)
        remover = functools.partial(_remove, target=target)
        app.connect('build-finished', remover)


def _remove(app, exception, target):
    os.remove(target)
