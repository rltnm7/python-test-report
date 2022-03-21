import pytest
from io import StringIO
from py.xml import html
from tests import conftest


def enclose_dq(val):
    return '"%s"' % val


class TestConftest:

    input_docstring_1 = """
    Test Docstring

    Inputs
    ------
    input string

    Expects
    -------
    expect string
    """

    expect_parse_1 = {
        "Descriptions": "Test Docstring",
        "Inputs": "input string",
        "Expects": "expect string\n"
    }

    input_docstring_2 = """Test Docstring

    Inputs
    ------
    input string

    Expects
    -------
    expect string
    """

    input_docstring_3 = """Test Docstring
    Inputs
    ------
    input string
    Expects
    -------
    expect string
    """

    input_pyproject = """[tool.poetry]
name = "test-pyhon-test-report"
version = "1.2.3"
description = ""
authors = ["rltnm7 <rltnm7@gmail.com>"]
packages = [
    { include = "src" }
]

[tool.poetry.dependencies]
python = "^3.9"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""

    @pytest.mark.parametrize(
        "key, expected",
        [
            ("version", "1.2.3"),
            ("name", "test-pyhon-test-report"),
        ],
        ids=enclose_dq
    )
    def test_read_pyproject(self, mocker, key, expected):
        mocked_open = mocker.patch("builtins.open")
        mocked_open.return_value = StringIO(self.input_pyproject)
        result = conftest._read_pyproject(key)
        assert result == expected

    @pytest.mark.parametrize(
        "x, expected",
        [
            ("", ""),
            ("    ", ""),
            ("\n", ""),
            ("    \n", ""),
            ("    Inputs", "Inputs"),
            ("Inputs\n", "Inputs"),
            ("    Expects\n", "Expects")
        ],
        ids=enclose_dq
    )
    def test_parse_content(self, x, expected):
        """
        _parse_content
        with @pytest.mark.parametrize

        Inputs
        ------
        @pytest.mark.parametrize:0

        Expects
        --------
        @pytest.mark.parametrize:1
        """
        result = conftest._parse_content(x)
        assert result == expected

    @pytest.mark.parametrize(
        "docstring, expected",
        [
            (input_docstring_1, expect_parse_1),
            (input_docstring_2, expect_parse_1),
            (input_docstring_3, expect_parse_1)
        ],
        ids=enclose_dq
    )
    def test_parse(self, docstring, expected):
        """
        _parse
        with @pytest.mark.parametrize

        Inputs
        ------
        @pytest.mark.parametrize:0

        Expects
        --------
        @pytest.mark.parametrize:1
        """
        result = conftest._parse(docstring)
        assert result == expected

    @pytest.mark.parametrize(
        "nodeid, expected",
        [
            ("tests/test_sample.py::TestClass::test_function[\"arg1\"-\"arg2\"-\"exp1\"]",
             ["arg1", "arg2", "exp1"]),
            ("tests/test_sample.py::TestClass::test_function[\"'arg1'\"-\"'arg2'\"-\"exp1\"]",
             ["'arg1'", "'arg2'", "exp1"])
        ],
        ids=enclose_dq
    )
    def test_split_nodeid(self, nodeid, expected):
        """
        _parse
        with @pytest.mark.parametrize

        Inputs
        ------
        @pytest.mark.parametrize:0

        Expects
        --------
        @pytest.mark.parametrize:1
        """
        result = conftest._split_nodeid(nodeid)
        assert result == expected

    @pytest.mark.parametrize(
        "attr, nodeid, expected",
        [
            ("arg1",
             "tests/test_sample.py::TestClass::test_function[\"arg1\"-\"arg2\"-\"exp1\"]",
             "arg1"),
            ("@pytest.mark.parametrize:0",
             "tests/test_sample.py::TestClass::test_function[\"arg1\"-\"arg2\"-\"exp1\"]",
             "arg1"),
            ("@pytest.mark.parametrize:1",
             "tests/test_sample.py::TestClass::test_function[\"arg1\"-\"arg2\"-\"exp1\"]",
             "arg2"),
            ("@pytest.mark.parametrize:0:1",
             "tests/test_sample.py::TestClass::test_function[\"arg1\"-\"arg2\"-\"exp1\"]",
             "arg1, arg2")
        ],
        ids=enclose_dq
    )
    def test_convert_column(self, attr, nodeid, expected):
        """
        _parse
        with @pytest.mark.parametrize

        Inputs
        ------
        @pytest.mark.parametrize:0:1

        Expects
        --------
        @pytest.mark.parametrize:2
        """
        class MockTestReport:
            def __init__(self, nodeid):
                self.nodeid = nodeid

        report = MockTestReport(nodeid)
        result = conftest._convert_column(attr, report)
        assert result == expected

    def test_pytest_html_report_title(self, mocker):
        """
        pytest_html_report_title

        Expects
        --------
        report.title == pythontest
        """
        class MockTestReport:
            def __init__(self):
                self.title = None

        report = MockTestReport()

        mocked_open = mocker.patch("builtins.open")
        mocked_open.return_value = StringIO(self.input_pyproject)

        conftest.pytest_html_report_title(report)
        assert report.title == "test-pyhon-test-report"

    def test_pytest_configure(self, mocker):
        """
        pytest_configure

        Expects
        --------
        config._metadata["Version"] == "0.0.1"
        """
        class MockConfig:
            def __init__(self):
                self._metadata = {}

        config = MockConfig()

        mocked_open = mocker.patch("builtins.open")
        mocked_open.return_value = StringIO(self.input_pyproject)

        conftest.pytest_configure(config)
        assert config._metadata["Version"] == "1.2.3"

    def test_pytest_html_results_table_header(self):
        """
        pytest_html_results_table_header

        Inputs
        ------
        [
            "<th class=\"sortable result initial-sort\" col=\"result\">Result</th>",
            "<th class=\"sortable\" col=\"name\">Test</th>",
            "<th class=\"sortable\" col=\"duration\">Duration</th>"
        ]

        Expects
        --------
        [
            "<th class=\"sortable\" col=\"name\">Test</th>",
            html.th("Descriptions"),
            html.th("Inputs"),
            html.th("Expects"),
            "<th class=\"sortable result initial-sort\" col=\"result\">Result</th>",
            "<th class=\"sortable\" col=\"duration\">Duration</th>"
        ]
        """

        cells = [
            "<th class=\"sortable result initial-sort\" col=\"result\">Result</th>",
            "<th class=\"sortable\" col=\"name\">Test</th>",
            "<th class=\"sortable\" col=\"duration\">Duration</th>"
        ]

        expected = [
            "<th class=\"sortable\" col=\"name\">Test</th>",
            html.th('Descriptions'),
            html.th('Inputs'),
            html.th('Expects'),
            "<th class=\"sortable result initial-sort\" col=\"result\">Result</th>",
            "<th class=\"sortable\" col=\"duration\">Duration</th>"
        ]

        conftest.pytest_html_results_table_header(cells)
        assert cells == expected

    def test_pytest_html_results_table_row(self):
        """
        pytest_html_results_table_row

        Inputs
        ------
        [
            "<td class=\"col-result\">Passed</td>",
            "<td class=\"col-name\">tests/test_conftest.py::TestConftest::test_pytest_html_results_table_row</td>",
            "<td class=\"col-duration\">0.00</td>"
        ]

        Expects
        -------
        [
            "<td class=\"col-name\">tests/test_conftest.py::TestConftest::test_pytest_html_results_table_row</td>",
            html.td(html.div("") + html.br(html.div("descriptions text"))),
            html.td(html.div("") + html.br(html.div("inputs text"))),
            html.td(html.div("") + html.br(html.div("expects text"))),
            "<td class=\"col-result\">Passed</td>",
            "<td class=\"col-duration\">0.00</td>"
        ]
        """

        cells = [
            "<td class=\"col-result\">Passed</td>",
            "<td class=\"col-name\">tests/test_conftest.py::TestConftest::test_pytest_html_results_table_row</td>",
            "<td class=\"col-duration\">0.00</td>"
        ]

        expected = [
            "<td class=\"col-name\">tests/test_conftest.py::TestConftest::test_pytest_html_results_table_row</td>",
            html.td(html.div("") + html.br(html.div("descriptions text"))),
            html.td(html.div("") + html.br(html.div("inputs text"))),
            html.td(html.div("") + html.br(html.div("expects text"))),
            "<td class=\"col-result\">Passed</td>",
            "<td class=\"col-duration\">0.00</td>"
        ]

        class MockTestReport:
            def __init__(self):
                self.descriptions = "descriptions text"
                self.inputs = "inputs text"
                self.expects = "expects text"

        report = MockTestReport()
        conftest.pytest_html_results_table_row(report, cells)
        assert cells == expected

    @pytest.mark.skip(reason='flake8_htmlの内部動作再現が困難なため')
    def test_pytest_runtest_makereport(self):
        """
        pytest_runtest_makereport
        """
        item = None
        conftest.pytest_runtest_makereport(item, None)
        assert False
