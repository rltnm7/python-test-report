# coding: UTF-8

import re


def parse(docstring):
    def _parse_content(x):
        return x.replace(" ", "").replace("\n", "")

    docstring = "Descriptions\n-\n" + docstring
    lines = [_parse_content(docline) for docline in docstring.splitlines() if docline != ""]
    matches = map(lambda x: re.compile(r"\s*-+").match(x), lines)
    key_indexes = [i-1 for i, x in enumerate(matches) if x is not None]

    docs = {}
    for s, e in zip(key_indexes, key_indexes[1:]+[len(lines)]):
        docs[lines[s]] = "\n".join(lines[s+2:e])

    return docs


docstring1 = """
        add関数のテスト
        aho

        Inputs
        ------
        @pytest.mark.parametrize: 2
        b

        Expects
        -------
        @pytest.mark.parametrize: 1
        a
"""


print(parse(docstring1))

docstring2 = """add関数のテスト
        aho

        Inputs
        ------
        @pytest.mark.parametrize: 2
        b

        Expects
        -------
        @pytest.mark.parametrize: 1
        a
"""

print(parse(docstring2))
