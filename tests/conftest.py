from py.xml import html
import os
import pytest
import re
from pytest_flake8 import Flake8Item


PROJECT_FILENAME = "pyproject.toml"
REPORT_COLUMNS = ["Descriptions", "Inputs", "Expects"]
PARAMETRIZE_MARKER = "@pytest.mark.parametrize"
PARAMETRIZE_MARKER_LENGTH = len(PARAMETRIZE_MARKER)


def _read_pyproject(key):
    """
    pyproject.tomlからkeyに該当するvalueを取得する

    Parameters
    ----------
    key: string
        読み取りデータのkey

    Returns
    -------
    string
        読み取りデータ
    """
    if os.path.exists(PROJECT_FILENAME):
        with open(PROJECT_FILENAME, "r") as f:
            for line in f.readlines():
                if key == line[:len(key)]:
                    return re.search(r'".*"', line).group()[1:-1]

def _parse_content(x):
    """
    文字列から改行および冒頭の複数スペースを削除する

    Parameters
    ----------
    x : string
        加工対象テキスト

    Returns
    -------
    string
        加工後テキスト
    """
    return re.sub(r"^\s*", "", x.replace("\n", ""))


def _parse(docstring):
    """
    docstringをディクショナリ型に変換する

    Parameters
    ----------
    docstring : string
        docstring型の文字列

    Returns
    -------
    dict
        変換後ディクショナリ
    """
    docstring = "%s\n-\n%s" % (REPORT_COLUMNS[0], docstring)
    lines = [_parse_content(docline) for docline in docstring.splitlines() if docline != ""]
    matches = map(lambda x: re.compile(r"\s*-+").match(x), lines)
    indexes = [i-1 for i, x in enumerate(matches) if x is not None]

    docs = {}
    for s, e in zip(indexes, indexes[1:]+[len(lines)]):
        docs[lines[s]] = "\n".join(lines[s+2:e])

    return docs


def _split_nodeid(nodeid):
    """
    nodeid型文字列を分割する

    Parameters
    ----------
    nodeid : string
        pytest.mark.parametrizeにより生成されるnodeid文字列

    Returns
    -------
    list of string
        nodeidを分割した配列
    """
    dlm = nodeid[-2]
    params = nodeid[nodeid.find("[")+2:-2].split(dlm)
    return [param for param in params if param != "-"]


def _convert_column(attr, report):
    """
    attrが@pytest.mark.parametrizeから始まる場合、
    続くインデックス番号の文字配列をnodeidから取り出し、カンマ区切り文字列として返す。
    attrがその他の文字列の場合は何も処理せずに返す。

    Parameters
    ----------
    attr : string
        変換対象文字列
    report : _pytest.reports.TestReport
        pytestが生成するレポートオブジェクト

    Returns
    -------
    string
        変換結果文字列
    """
    if(attr[:PARAMETRIZE_MARKER_LENGTH] == PARAMETRIZE_MARKER):
        indexes = list(map(int, attr[PARAMETRIZE_MARKER_LENGTH+1:].split(":")))

        if len(indexes) == 1:
            params = (_split_nodeid(report.nodeid))[indexes[0]]
            return params

        elif len(indexes) == 2:
            params = (_split_nodeid(report.nodeid))[indexes[0]:indexes[1]+1]
            return ", ".join(params)

    else:
        return attr


def pytest_configure(config):
    """
    バージョンを設定する

    Parameters
    ----------
    report : _pytest.reports.TestReport
        pytestが生成するレポートオブジェクト

    See Also
    --------
    pytest.hookspec.pytest_configure:
        https://docs.pytest.org/en/6.2.x/reference.html#pytest.hookspec.pytest_configure
    """
    config._metadata["Version"] = _read_pyproject("version")


def pytest_html_report_title(report):
    """
    レポートタイトルを設定する

    Parameters
    ----------
    report : _pytest.reports.TestReport
        pytestが生成するレポートオブジェクト
    """
    report.title = _read_pyproject("name")


def pytest_html_results_table_header(cells):
    """
    テスト結果テーブルヘッダを設定する

    Parameters
    ----------
    cells : list of py._xmlgen.th
        テーブルヘッダ配列
    """
    result = cells.pop(0)
    duration = cells.pop(1)
    del cells[1:]

    for column in REPORT_COLUMNS:
        cells.append(html.th(column))

    cells.append(result)
    cells.append(duration)


def pytest_html_results_table_row(report, cells):
    """
    テスト結果をテーブルへ登録する

    Parameters
    ----------
    cells : list of py._xmlgen.td
        テーブル配列
    """
    result = cells.pop(0)
    duration = cells.pop(1)
    del cells[1:]

    for column in REPORT_COLUMNS:
        attr = getattr(report, column.lower(), "-")
        content = html.div("")
        for column in _convert_column(attr, report).split("\n"):
            content += html.br(html.div(column))
        cells.append(html.td(content))

    cells.append(result)
    cells.append(duration)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    docstringからレポートオブジェクトを生成する

    Parameters
    ----------
    item : Item
        テスト結果オブジェクト
    call : CallInfo
        The CallInfo for the phase

    See Also
    --------
    pytest.hookspec.pytest_runtest_makereport:
        https://docs.pytest.org/en/6.2.x/reference.html#pytest.hookspec.pytest_runtest_makereport
    """
    outcome = yield
    report = outcome.get_result()

    if(type(item) == pytest.Function):
        docstring = _parse(str(item.function.__doc__))
        for key, value in docstring.items():
            setattr(report, key.lower(), value)

    elif(type(item) == Flake8Item):
        # contest.pyをtests配下に置くとFLAKE8ではpytest_runtest_makereportが呼ばれない
        setattr(report, REPORT_COLUMNS[0].lower(), "FLAKE8")
