# -*- coding: UTF-8 -*-
"""
Additional unit tests for the :mod`parse` module.
Related to auto-detection of number base (base=10, 2, 8, 16).
"""
import pytest
import parse

def assert_parse_number_with_format_d(text, expected):
    parser = parse.Parser("{value:d}")
    result = parser.parse(text)
    assert result.named == dict(value=expected)


@pytest.mark.parametrize("text, expected", [
    ("123", 123)
])
def test_parse_number_with_base10(text, expected):
    assert_parse_number_with_format_d(text, expected)

@pytest.mark.parametrize("text, expected", [
    ("0b0", 0),
    ("0b1011", 11),
])
def test_parse_number_with_base2(text, expected):
    assert_parse_number_with_format_d(text, expected)

@pytest.mark.parametrize("text, expected", [
    ("0o0", 0),
    ("0o10", 8),
    ("0o12", 10),
])
def test_parse_number_with_base8(text, expected):
    assert_parse_number_with_format_d(text, expected)

@pytest.mark.parametrize("text, expected", [
    ("0x0", 0),
    ("0x01", 1),
    ("0x12", 18),
])
def test_parse_number_with_base16(text, expected):
    assert_parse_number_with_format_d(text, expected)
