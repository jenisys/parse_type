# -*- coding: utf-8 -*-
"""
Provides support for cardinality fields.
A cardinality field is a type suffix for parse format expression, ala:

    "... {person:Person?} ..."   -- OPTIONAL: Cardinality zero or one, 0..1
    "... {persons:Person*} ..."  -- MANY0: Cardinality zero or more, 0..
    "... {persons:Person+} ..."  -- MANY:  Cardinality one  or more, 1..
"""

from __future__ import absolute_import
from .cardinality import Cardinality, TypeBuilder


class MissingTypeError(KeyError):
    pass

# -----------------------------------------------------------------------------
# CLASS: Cardinality (Field Part)
# -----------------------------------------------------------------------------
class CardinalityField(object):
    """
    Cardinality field for parse format expression, ala:

        "... {person:Person?} ..."   -- OPTIONAL: Cardinality zero or one, 0..1
        "... {persons:Person*} ..."  -- MANY0: Cardinality zero or more, 0..
        "... {persons:Person+} ..."  -- MANY:  Cardinality one  or more, 1..

    STATUS: IDEA, currently not accepted in :mod:`parse` module.
    """

    # -- MAPPING SUPPORT:
    pattern_chars = "?*+"
    from_char_map = {
        '?': Cardinality.zero_or_one,
        '*': Cardinality.zero_or_more,
        '+': Cardinality.one_or_more,
    }
    to_char_map = dict([(value, key)  for key, value in from_char_map.items()])

    @classmethod
    def matches_type_name(cls, type_name):
        """
        Checks if a type name uses the CardinalityField naming scheme.

        :param type_name:  Type name to check (as string).
        :return: True, if type name has CardinalityField name suffix.
        """
        return type_name and type_name[-1] in CardinalityField.pattern_chars

    @classmethod
    def type_basename(cls, type_name):
        """
        Extracts the underlying type
        """
        if cls.matches_type_name(type_name):
            return type_name[:-1]
        else:
            # -- ASSUME: Cardinality.one
            return type_name

# -----------------------------------------------------------------------------
# CLASS: CardinalityFieldTypeBuilder
# -----------------------------------------------------------------------------
class CardinalityFieldTypeBuilder(object):
    """
    Utility class to create type converters based on:

      * the CardinalityField naming scheme and
      * type converter for cardinality=1
    """

    listsep = ','

    @classmethod
    def create_type_variant(cls, type_name, type_converter):
        """
        Create type variants for types with a cardinality field.
        The new type converters are based on the type converter with
        cardinality=1.

        .. code-block:: python

            import parse

            @parse.with_pattern(r"\d+")
            def parse_number(text):
                return int(text)

            new_type = CardinalityFieldTypeBuilder.create_type_variant(
                                    "Number+", parse_number)
            new_type = CardinalityFieldTypeBuilder.create_type_variant(
                                    "Number+", dict(Number=parse_number))

        :param type_name:  Type name with cardinality field suffix.
        :param type_converter:  Type converter or type dictionary.
        :return: Type converter variant (function).
        :raises: ValueError, if type_name does not end with CardinalityField
        :raises: MissingTypeError, if type_converter is missing in type_dict
        """
        assert isinstance(type_name, str)
        if not CardinalityField.matches_type_name(type_name):
            message = "type_name='%s' has no CardinalityField" % type_name
            raise ValueError(message)

        cardinality_char = type_name[-1]
        cardinality = CardinalityField.from_char_map[cardinality_char]
        if isinstance(type_converter, dict):
            type_dict = type_converter
            type_name_one = type_name[:-1]
            type_converter = type_dict.get(type_name_one, None)
            if not type_converter:
                raise MissingTypeError(type_name_one)

        assert callable(type_converter)
        type_variant = TypeBuilder.with_cardinality(cardinality,
                                    type_converter, cls.listsep)
        type_variant.name = type_name
        return type_variant


    @classmethod
    def create_type_variants(cls, type_names, type_dict):
        """
        Create type variants for types with a cardinality field.
        The new type converters are based on the type converter with
        cardinality=1.

        .. code-block:: python

            import parse

            @parse.with_pattern(r"\d+")
            def parse_number(text):
                return int(text)

            new_types = CardinalityFieldTypeBuilder.create_type_variants(
                            ["Number?", "Number+"], dict(Number=parse_number))

        :param type_names: List of type names with cardinality field suffix.
        :param type_dict:  Type dictionary with named type converters.
        :return: Type dictionary with type converter variants.
        """
        type_variant_dict = {}
        for type_name in type_names:
            type_variant = cls.create_type_variant(type_name, type_dict)
            type_variant_dict[type_name] = type_variant
        return type_variant_dict

    # XXX-JE-TODO: Check if really needed.
    @classmethod
    def create_missing_type_variants(cls, type_names, type_dict):
        """
        Create missing type variants for types with a cardinality field.

        :param type_names: List of type names with cardinality field suffix.
        :param type_dict:  Type dictionary with named type converters.
        :return: Type dictionary with missing type converter variants.
        """
        missing_type_names = [ name for name in type_names
                               if name not in type_dict ]
        return cls.create_type_variants(missing_type_names, type_dict)
