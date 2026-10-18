from unittest.mock import patch

import pytest

from log import log


def test_log(capsys: pytest.CaptureFixture[str]) -> None:
    @log('add — {}с!')
    def add(left: int, right: int) -> int:
        return left + right

    with patch('log.random.randint', return_value=3) as randint:
        result: int = add(2, right=3)
        assert result == 5
        randint.assert_called_once_with(1, 5)

    assert capsys.readouterr().out == 'add — 3с!\n'
    assert add.__name__ == 'add'


def test_template(capsys: pytest.CaptureFixture[str]) -> None:
    @log('Выполнено за {}с!')
    def double(value: int) -> int:
        return value * 2

    with patch('log.random.randint', return_value=2):
        assert double(4) == 8

    assert capsys.readouterr().out == 'Выполнено за 2с!\n'


def test_wrapped(capsys: pytest.CaptureFixture[str]) -> None:
    @log('Выполнено за {}с!')
    def double(value: int) -> int:
        return value * 2

    assert getattr(double, '__wrapped__')(4) == 8
    assert capsys.readouterr().out == ''
