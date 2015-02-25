"""
Sphinx plugin to add links to the changelog.
"""

import re
import os
import operator

import six


class Repl:

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
    def __init__(self, defn):
        vars(self).update(defn)

    def matches(self, text):
        return re.match(self.pattern+'$', text)


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
        repls = map(Repl, defn.get('replace', []))
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
        ns = match.groupdict()
        ns.update(vars(self))
        ns.update(vars(repl))
        hyperlink = '`{text} <{href}>`_'
        return hyperlink.format(text=text, href=repl.url.format(**ns))

    def write_links(self, source, target):
        with open(source) as source:
            out = self.run(source.read())
        with open(target, 'w') as dest:
            dest.write(out)


def setup(app):
    app.add_config_value('link_files', {}, '')
    app.connect('builder-inited', make_links)

def _extend_name(filename):
    base, ext = os.path.splitext(filename)
    return base + ' (links)' + ext

def make_links(app):
    files_def = app.config.link_files
    for filename, defn in files_def.items():
        replacer = Replacer.from_definition(defn)
        target = _extend_name(filename)
        replacer.write_links(filename, target)
    app.connect('build-finished', remove_targets)

def remove_targets(app, exception):
    files_def = app.config.link_files
    for filename in files_def:
        target = _extend_name(filename)
        os.remove(target)
