# -*- coding: utf-8 -*-

from parse_type import TypeBuilder
import unittest

# -----------------------------------------------------------------------------
# TEST SUPPORT FOR: TypeBuilder Tests
# -----------------------------------------------------------------------------
# -- PROOF-OF-CONCEPT DATATYPE:
def parse_number(text):
    return int(text)
parse_number.pattern = r"\d+"   # Provide better regexp pattern than default.
parse_number.name = "Number"    # For testing only.

# -- ENUM DATATYPE:
parse_yesno = TypeBuilder.make_enum({
    "yes":  True,   "no":  False,
    "on":   True,   "off": False,
    "true": True,   "false": False,
})
parse_yesno.name = "YesNo"      # For testing only.

# -- ENUM DATATYPE:
parse_person_choice = TypeBuilder.make_choice(["Alice", "Bob", "Charly"])
parse_person_choice.name = "PersonChoice"      # For testing only.


# -----------------------------------------------------------------------------
# ABSTRACT TEST CASE: TestParseType
# -----------------------------------------------------------------------------
class ParseTypeTestCase(unittest.TestCase):
    """
    Common test case base class for :mod:`parse_type` tests.
    """

    # -- PYTHON VERSION BACKWARD-COMPATIBILTY:
    if not hasattr(unittest.TestCase, "assertIsNone"):
        def assertIsNone(self, obj, msg=None):
            self.assert_(obj is None, msg)

        def assertIsNotNone(self, obj, msg=None):
            self.assert_(obj is not None, msg)

    #@staticmethod
    #def build_type_dict(type_converters):
    #    """
    #    XXX
    #    Builds type dictionary for user-defined type converters, used by parse.
    #    :param type_converters: List of type-converters (parse_types)
    #    :return: Type-converter dictionary
    #    """
    #    more_types = {}
    #    for type_converter in type_converters:
    #        more_types[type_converter.name] = type_converter
    #    return more_types

    def assert_match(self, parser, text, param_name, expected):
        """
        Check that a parser can parse the provided text and extracts the
        expected value for a parameter.

        :param parser: Parser to use
        :param text:   Text to parse
        :param param_name: Name of parameter
        :param expected:   Expected value of parameter.
        :raise: AssertationError on failures.
        """
        result = parser.parse(text)
        self.assertIsNotNone(result)
        self.assertEqual(result[param_name], expected)

    def assert_mismatch(self, parser, text, param_name):
        """
        Check that a parser cannot extract the parameter from the provided text.
        A parse mismatch has occured.

        :param parser: Parser to use
        :param text:   Text to parse
        :param param_name: Name of parameter
        :raise: AssertationError on failures.
        """
        result = parser.parse(text)
        self.assertIsNone(result)


# Copyright (c) 2012-2013 by Jens Engel (https://github/jenisys/)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
