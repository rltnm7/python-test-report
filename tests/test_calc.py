import pytest
from src.calc import Calc


def enclose_dq(val):
    return '"%s"' % val


class TestCalc:

    @classmethod
    def setup_class(cls):
        print("\nTestCalc Start.")
        cls.calc = Calc()

    @classmethod
    def teardown_class(cls):
        del cls.calc
        print("\nTestCalc End.")

    def setup_method(self, method):
        print('\nStart Method: %s' % method.__name__)

    def teardown_method(self, method):
        print('\nEnd Method: %s' % method.__name__)

    def test_add(self):
        """
        add関数のテスト

        Inputs
        ------
        1234567890, 987654321

        Expects
        -------
        2222222211
        """
        left, right = 1234567890, 987654321
        expected = 2222222211

        result = self.calc.add(left, right)
        assert result == expected

    @pytest.mark.parametrize(
        "left, right, expected",
        [
            (-1, -1, -2),
            (-1, 0, -1),
            (-1, 1, 0),
            (0, -1, -1),
            (0, 0, 0),
            (0, 1, 1),
            (1, -1, 0),
            (1, 0, 1),
            (1, 1, 2),
        ],
        ids=enclose_dq)
    def test_add_variation(self, left, right, expected):
        """
        add関数のテスト
        with @pytest.mark.parametrize

        Inputs
        ------
        @pytest.mark.parametrize: 0:1

        Expects
        -------
        @pytest.mark.parametrize: 2
        """
        result = self.calc.add(left, right)
        assert result == expected

    def test_sub(self):
        """
        sub関数のテスト

        Inputs
        ------
        1234567890, 987654321

        Expects
        -------
        246913569
        """
        left, right = 1234567890, 987654321
        expected = 246913569

        actual = self.calc.sub(left, right)
        assert actual == expected

    @pytest.mark.parametrize(
        "left, right, expected",
        [
            (-1, -1, 0),
            (-1, 0, -1),
            (-1, 1, -2),
            (0, -1, 1),
            (0, 0, 0),
            (0, 1, -1),
            (1, -1, 2),
            (1, 0, 1),
            (1, 1, 0),
        ],
        ids=enclose_dq)
    def test_sub_variation(self, left, right, expected):
        """
        sub関数のテスト
        with @pytest.mark.parametrize

        Inputs
        ------
        @pytest.mark.parametrize: 0:1

        Expects
        -------
        @pytest.mark.parametrize: 2
        """
        actual = self.calc.sub(left, right)
        assert actual == expected

    def test_mul(self):
        """
        mul関数のテスト

        Inputs
        ------
        12345, 67890

        Expects
        -------
        838102050
        """
        left, right = 12345, 67890
        expected = 838102050

        actual = self.calc.mul(left, right)
        assert actual == expected

    @pytest.mark.parametrize(
        "left, right, expected",
        [
            (-1, -1, 1),
            (-1, 0, 0),
            (-1, 1, -1),
            (0, -1, 0),
            (0, 0, 0),
            (0, 1, 0),
            (1, -1, -1),
            (1, 0, 0),
            (1, 1, 1),
        ],
        ids=enclose_dq)
    def test_mul_variation(self, left, right, expected):
        """
        mul関数のテスト
        with @pytest.mark.parametrize

        Inputs
        ------
        @pytest.mark.parametrize: 0:1

        Expects
        -------
        @pytest.mark.parametrize: 2
        """
        actual = self.calc.mul(left, right)
        assert actual == expected

    def test_div(self):
        """
        div関数のテスト

        Inputs
        ------
        838102050, 67890

        Expects
        -------
        12345
        """
        left, right = 838102050, 67890
        expected = 12345

        actual = self.calc.div(left, right)
        assert actual == expected

    @pytest.mark.parametrize(
        "left, right, expected",
        [
            (-1, -1, 1),
            (-1, 1, -1),
            (0, -1, 0),
            (0, 1, 0),
            (1, -1, -1),
            (1, 1, 1),
        ],
        ids=enclose_dq)
    def test_div_variation(self, left, right, expected):
        """
        div関数のテスト
        with @pytest.mark.parametrize

        Inputs
        ------
        @pytest.mark.parametrize: 0:1

        Expects
        -------
        @pytest.mark.parametrize: 2
        """
        actual = self.calc.div(left, right)
        assert actual == expected
