import pytest

import rst.linker


@pytest.fixture
def linker_example():
    return {
        'CHANGES.rst': dict(
            using = dict(
                kiln='https://org.kilnhg.com/Code/Repositories'
            ),
            replace = [
                dict(
                    pattern=r"proj (?P<proj_ver>\d+(\.\d+)*([abc]\d+)?)",
                    url='{kiln}/repo/proj/Files/CHANGES?rev={proj_ver}',
                ),
                dict(
                    pattern=r"(Case |#)(?P<id>\d+)",
                    url='https://org.fogbugz.com/f/cases/{id}/',
                ),
            ],
        )
    }

def test_linker_example(linker_example):
    defn = linker_example['CHANGES.rst']
    repl = rst.linker.Replacer.from_definition(defn)
    assert 'kilnhg' in repl.run("""
        proj 1.0 was released
        """)
