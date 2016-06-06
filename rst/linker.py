"""
Sphinx plugin to add links and timestamps to the changelog.
"""

from __future__ import unicode_literals

import re
import os
import operator
import subprocess
import io

import dateutil.parser

import six
map = six.moves.map
filter = six.moves.filter


class Repl(object):
    @classmethod
    def from_defn(cls, defn):
        "Return the first Repl subclass that works with this"
        instances = (subcl(defn) for subcl in cls.__subclasses__())
        return next(filter(None, instances))

    def __init__(self, defn):
        vars(self).update(defn)

    def matches(self, text):
        return re.match(self.pattern+'$', text)

    def __bool__(self):
        return False

    def __nonzero__(self):
        # Python 2.7 compatibility
        return self.__bool__()


class URLLinker(Repl):
    """
    Each replacement should have the form:

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
    """
    Replace content with a version number to include the date stamp
    from the SCM.

    For example, consider a changelog with the following:

        1.0
        ---

        Changed something.

    The following replacement definition would add a datestamp
    after the heading:

    {
        pattern: r"^(?m)((?P<scm_version>\d+(\.\d+){1,2})\n-+\n)",
        with_scm: "{text}\nTagged {rev[timestamp]}\n",
    }

    If the scm_version is detected, a timestamp will be added to the
    namespace.

    If detected, the rev[timestamp] is a datetime-aware timestamp,
    so arbitrary formatting operators may be applied to it, such as
    the following which will render as "Dec 2000":

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
    def _get_scm_info_for(scm_version):
        scm = 'hg' if os.path.isdir('.hg') else 'git'
        commands = dict(
            hg=['hg', 'log', '-l', '1', '--template', '{date|isodate}', '-r', scm_version],
            git=['git', 'log', '-1', '--format=%ai', scm_version],
        )
        cmd = commands[scm]
        try:
            with open(os.devnull, 'w') as devnull:
                ts = subprocess.check_output(cmd, stderr=devnull).decode('utf-8').strip()
            assert ts
            ts = dateutil.parser.parse(ts)
        except Exception:
            return
        return dict(timestamp=ts)

    def __bool__(self):
        return 'with_scm' in vars(self)


class Replacer(list):
    @staticmethod
    def load(filename):
        defn = dict()
        with open(filename) as stream:
            six.exec_(stream.read(), defn)
        return defn

    @classmethod
    def from_definition(cls, defn):
        """
        A definition may contain the following members:

        - using: a dictionary of variables available for substitution
        - replace: a list of replacement definitions.
        """
        repls = map(Repl.from_defn, defn.get('replace', []))
        self = cls(repls)
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
        with io.open(source, encoding='utf-8') as source:
            out = self.run(source.read())
        with io.open(target, 'w', encoding='utf-8') as dest:
            dest.write(out)


def setup(app):
    app.add_config_value(str('link_files'), {}, '')
    app.connect(str('builder-inited'), make_links)

def _extend_name(filename):
    base, ext = os.path.splitext(filename)
    return base + ' (links)' + ext

def make_links(app):
    files_def = app.config.link_files
    for filename, defn in files_def.items():
        replacer = Replacer.from_definition(defn)
        target = _extend_name(filename)
        replacer.write_links(filename, target)
    app.connect(str('build-finished'), remove_targets)

def remove_targets(app, exception):
    files_def = app.config.link_files
    for filename in files_def:
        target = _extend_name(filename)
        os.remove(target)
