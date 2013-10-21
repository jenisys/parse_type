#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test experiment for parse.
Add cardinality format field after type:

    "... {person:Person?} ..."   -- CARDINALITY: Zero or one,  0..1 (optional)
    "... {persons:Person*} ..."  -- CARDINALITY: Zero or more, 0..N (many0)
    "... {persons:Person+} ..."  -- CARDINALITY: One or more,  1..N (many)


REQUIRES:
    parse >= 1.5.3.1 ('pattern' attribute support and further extensions)

STATUS:
    IDEA, working prototype with patched parse module, but not accepted.
"""

from __future__ import absolute_import
from .parse_type_test \
    import ParseTypeTestCase, TestCase, parse_number, unittest
from .test_cardinality import CardinalityTypeBuilderTest
from parse_type import Cardinality
from parse_type.cardinality_field \
    import CardinalityField, CardinalityFieldTypeBuilder, MissingTypeError
import parse


# -------------------------------------------------------------------------
# TEST CASE: TestParseTypeWithCardinalityField
# -------------------------------------------------------------------------
class TestCardinalityField(TestCase):
    VALID_TYPE_NAMES = ["Number?", "Number*", "Number+"]
    INVALID_TYPE_NAMES = ["?Invalid", "Inval*d", "In+valid"]

    def test_pattern_chars(self):
        for pattern_char in CardinalityField.pattern_chars:
            self.assertIn(pattern_char, CardinalityField.from_char_map)

    def test_to_from_char_map_symmetry(self):
        for cardinality, char in CardinalityField.to_char_map.items():
            self.assertEqual(cardinality, CardinalityField.from_char_map[char])
        for char, cardinality in CardinalityField.from_char_map.items():
            self.assertEqual(char, CardinalityField.to_char_map[cardinality])

    def test_matches_type_name(self):
        for type_name in self.VALID_TYPE_NAMES:
            self.assertTrue(CardinalityField.matches_type_name(type_name))

        for type_name in self.INVALID_TYPE_NAMES:
            self.assertFalse(CardinalityField.matches_type_name(type_name))

    def test_type_basename__with_valid_types(self):
        for type_name in self.VALID_TYPE_NAMES:
            expected = type_name[:-1]
            self.assertEqual(CardinalityField.type_basename(type_name), expected)

    def test_type_basename__with_invalid_types(self):
        for type_name in self.INVALID_TYPE_NAMES:
            expected = type_name
            self.assertEqual(CardinalityField.type_basename(type_name), expected)


# -------------------------------------------------------------------------
# TEST CASE:
# -------------------------------------------------------------------------
class TestCardinalityFieldTypeBuilder(CardinalityTypeBuilderTest):
    INVALID_TYPE_DICT_DATA = [
        (dict(),                        "empty type_dict"),
        (dict(NumberX=parse_number),    "non-empty type_dict (wrong name)"),
    ]

    # -- UTILITY METHODS:
    def generate_type_variants(self,type_name):
        for pattern_char in CardinalityField.pattern_chars:
            special_name = "%s%s" % (type_name.strip(), pattern_char)
            self.assertTrue(CardinalityField.matches_type_name(special_name))
            yield special_name

    # -- METHOD: CardinalityFieldTypeBuilder.create_type_variant()
    def test_create_type_variant__with_many_and_type_converter(self):
        type_builder = CardinalityFieldTypeBuilder
        parse_candidate = type_builder.create_type_variant("Number+",
                                                type_converter=parse_number)
        self.check_parse_number_with_many(parse_candidate, "Number+")

    def test_create_type_variant__with_optional_and_type_dict(self):
        type_builder = CardinalityFieldTypeBuilder
        parse_candidate = type_builder.create_type_variant("Number?",
                                                dict(Number=parse_number))
        self.check_parse_number_with_optional(parse_candidate, "Number?")

    def test_create_type_variant__with_many_and_type_dict(self):
        type_builder = CardinalityFieldTypeBuilder
        parse_candidate = type_builder.create_type_variant("Number+",
                                                dict(Number=parse_number))
        self.check_parse_number_with_many(parse_candidate, "Number+")

    def test_create_type_variant__with_many0_and_type_dict(self):
        type_builder = CardinalityFieldTypeBuilder
        parse_candidate = type_builder.create_type_variant("Number*",
                                                dict(Number=parse_number))
        self.check_parse_number_with_many0(parse_candidate, "Number*")

    def test_create_type_variant__can_create_all_variants(self):
        type_builder = CardinalityFieldTypeBuilder
        for special_name in self.generate_type_variants("Number"):
            # -- CASE: type_converter
            parse_candidate = type_builder.create_type_variant(special_name,
                                                               parse_number)
            self.assertTrue(callable(parse_candidate))

            # -- CASE: type_dict
            parse_candidate = type_builder.create_type_variant(special_name,
                                                    dict(Number=parse_number))
            self.assertTrue(callable(parse_candidate))

    def test_create_type_variant__raises_error_with_invalid_type_name(self):
        type_builder = CardinalityFieldTypeBuilder
        for invalid_type_name in TestCardinalityField.INVALID_TYPE_NAMES:
            with self.assertRaises(ValueError):
                type_builder.create_type_variant(invalid_type_name,
                                                 parse_number)

    def test_create_type_variant__raises_error_with_missing_primary_type(self):
        type_builder = CardinalityFieldTypeBuilder
        for special_name in self.generate_type_variants("Number"):
            for type_dict, description in self.INVALID_TYPE_DICT_DATA:
                with self.assertRaises(MissingTypeError):
                    type_builder.create_type_variant(special_name, type_dict)


    # -- METHOD: CardinalityFieldTypeBuilder.create_type_variants()
    def test_create_type_variants__all(self):
        type_builder = CardinalityFieldTypeBuilder
        special_names = ["Number?", "Number+", "Number*"]
        type_dict = dict(Number=parse_number)
        new_types = type_builder.create_type_variants(special_names, type_dict)
        self.assertSequenceEqual(set(new_types.keys()), set(special_names))
        self.assertEqual(len(new_types), 3)

        parse_candidate = new_types["Number?"]
        self.check_parse_number_with_optional(parse_candidate, "Number?")
        parse_candidate = new_types["Number+"]
        self.check_parse_number_with_many(parse_candidate, "Number+")
        parse_candidate = new_types["Number*"]
        self.check_parse_number_with_many0(parse_candidate, "Number*")

    def test_create_type_variants__raises_error_with_invalid_type_name(self):
        type_builder = CardinalityFieldTypeBuilder
        for invalid_type_name in TestCardinalityField.INVALID_TYPE_NAMES:
            type_dict = dict(Number=parse_number)
            with self.assertRaises(ValueError):
                type_names = [invalid_type_name]
                type_builder.create_type_variants(type_names, type_dict)

    def test_create_missing_type_variants__raises_error_with_missing_primary_type(self):
        type_builder = CardinalityFieldTypeBuilder
        for special_name in self.generate_type_variants("Number"):
            for type_dict, description in self.INVALID_TYPE_DICT_DATA:
                self.assertNotIn("Number", type_dict)
                with self.assertRaises(MissingTypeError):
                    names = [special_name]
                    type_builder.create_type_variants(names, type_dict)


    # -- METHOD: CardinalityFieldTypeBuilder.create_missing_type_variants()
    def test_create_missing_type_variants__all_missing(self):
        type_builder = CardinalityFieldTypeBuilder
        missing_names = ["Number?", "Number+", "Number*"]
        new_types = type_builder.create_missing_type_variants(missing_names,
                                                    dict(Number=parse_number))
        self.assertSequenceEqual(set(new_types.keys()), set(missing_names))
        self.assertEqual(len(new_types), 3)

    def test_create_missing_type_variants__none_missing(self):
        # -- PREPARE: Create all types and store them in the type_dict.
        type_builder = CardinalityFieldTypeBuilder
        type_names     = ["Number?", "Number+", "Number*"]
        all_type_names = ["Number", "Number?", "Number+", "Number*"]
        type_dict = dict(Number=parse_number)
        new_types = type_builder.create_missing_type_variants(type_names,
                                                                type_dict)
        type_dict.update(new_types)
        self.assertSequenceEqual(set(new_types.keys()), set(type_names))
        self.assertSequenceEqual(set(type_dict.keys()), set(all_type_names))

        # -- TEST: All special types are already stored in the type_dict.
        new_types2 = type_builder.create_missing_type_variants(type_names,
                                                                type_dict)
        self.assertEqual(len(new_types2), 0)

    def test_create_missing_type_variants__some_missing(self):
        # -- PREPARE: Create some types and store them in the type_dict.
        type_builder = CardinalityFieldTypeBuilder
        special_names  = ["Number?", "Number+", "Number*"]
        type_names1    = ["Number?", "Number*"]
        type_names2    = special_names
        type_dict = dict(Number=parse_number)
        new_types = type_builder.create_missing_type_variants(type_names1,
                                                                type_dict)
        type_dict.update(new_types)
        self.assertSequenceEqual(set(new_types.keys()), set(type_names1))
        self.assertSequenceEqual(set(type_dict.keys()),
                                set(["Number", "Number?", "Number*"]))

        # -- TEST: All special types are already stored in the type_dict.
        new_types2 = type_builder.create_missing_type_variants(type_names2,
                                                                type_dict)
        self.assertEqual(len(new_types2), 1)
        self.assertSequenceEqual(set(new_types2.keys()), set(["Number+"]))

    def test_create_type_variant__raises_error_with_invalid_type_name(self):
        type_builder = CardinalityFieldTypeBuilder
        for invalid_type_name in TestCardinalityField.INVALID_TYPE_NAMES:
            type_dict = dict(Number=parse_number)
            with self.assertRaises(ValueError):
                type_names = [invalid_type_name]
                type_builder.create_missing_type_variants(type_names, type_dict)

    def test_create_missing_type_variants__raises_error_with_missing_primary_type(self):
        type_builder = CardinalityFieldTypeBuilder
        for special_name in self.generate_type_variants("Number"):
            for type_dict, description in self.INVALID_TYPE_DICT_DATA:
                self.assertNotIn("Number", type_dict)
                with self.assertRaises(MissingTypeError):
                    names = [special_name]
                    type_builder.create_missing_type_variants(names, type_dict)


# -----------------------------------------------------------------------------
# MAIN:
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()


# Copyright (c) 2012-2013 by Jens Engel (https://github/jenisys/parse_type)
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
