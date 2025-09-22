from parser import Parser

import pytest

from evaluator import Evaluator
from lexer import Lexer


def _eval(string: str, symbol_table: dict):
    lexer = Lexer(string)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    evaluator = Evaluator(ast, symbol_table)
    evaluator.evaluate()

    return evaluator


@pytest.mark.parametrize(
    "input_str, symbol_table, expected_str,"
    "expected_symbol_table, expected_identifier",
    [
        pytest.param(
            "a=1",
            {},
            "a 1 =",
            {"a": 1},
            "a",
            id="simple",
        ),
        pytest.param(
            "a=4+7*3",
            {},
            "a 4 7 3 * + =",
            {"a": 25},
            "a",
            id="complex",
        ),
        pytest.param(
            "a=b+5",
            {"b": 3},
            "a b 5 + =",
            {"a": 8, "b": 3},
            "a",
            id="symbol_table",
        ),
        pytest.param(
            "a=0-5",
            {},
            "a 0 5 - =",
            {"a": -5},
            "a",
            id="negative_via_subtraction",
        ),
        pytest.param(
            "a=-5",
            {},
            "a 5 u- =",
            {"a": -5},
            "a",
            id="direct_negative_number",
        ),
        pytest.param(
            "a=+7",
            {},
            "a 7 u+ =",
            {"a": 7},
            "a",
            id="direct_positive_number",
        ),
    ],
)
def test_evaluator(
    input_str,
    symbol_table,
    expected_str,
    expected_symbol_table,
    expected_identifier,
):
    evaluator = _eval(input_str, symbol_table)

    assert str(evaluator) == expected_str

    identifier = evaluator.execute()
    assert symbol_table == expected_symbol_table
    assert identifier == expected_identifier


def test_undefined_reference():
    evaluator = _eval("a=b+3", {})

    with pytest.raises(NameError):
        evaluator.execute()
