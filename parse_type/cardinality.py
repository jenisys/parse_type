# -*- coding: utf-8 -*-
"""
This module simplifies to build parse types and regular expressions
for a data type with the specified cardinality.
"""

# -- USE: enum34
from enum import Enum


# -----------------------------------------------------------------------------
# CLASS: Cardinality (Enum Class)
# -----------------------------------------------------------------------------
class Cardinality(Enum):
    """
    Cardinality enumeration class to simplify building regular expression
    patterns for a data type with the specified cardinality.
    """
    __order__ = "one, zero_or_one, zero_or_more, one_or_more"
    one          = (None, )
    zero_or_one  = (r"(%s)?", )                # SCHEMA: pattern
    zero_or_more = (r"(%s)?(\s*%s\s*(%s))*", ) # SCHEMA: pattern listsep pattern
    one_or_more  = (r"(%s)(\s*%s\s*(%s))*", )  # SCHEMA: pattern listsep pattern

    # -- ALIASES:
    optional = zero_or_one
    many0 = zero_or_more
    many  = one_or_more

    def __init__(self, schema):
        self.schema = schema

    def make_pattern(self, pattern, listsep=','):
        """
        Make pattern for a data type with the specified cardinality.

        .. code-block:: python

            yes_no_pattern = r"yes|no"
            many_yes_no = Cardinality.one_or_more.make_pattern(yes_no_pattern)

        :param pattern:  Regular expression for type (as string).
        :param listsep:  List separator for multiple items (as string, optional)
        :return: Regular expression pattern for type with cardinality.
        """
        if self is Cardinality.one:
            return pattern
        elif self is Cardinality.zero_or_one:
            return self.schema % pattern
        else:
            return self.schema % (pattern, listsep, pattern)

    def is_many(self):
        """
        Checks for a more general interpretation of "many".
        :return: True, if Cardinality.zero_or_more or Cardinality.one_or_more.
        """
        return ((self is Cardinality.zero_or_more) or
                (self is Cardinality.one_or_more))


# -----------------------------------------------------------------------------
# CLASS: TypeBuilder
# -----------------------------------------------------------------------------
class TypeBuilder(object):
    """
    Provides a utility class to build type-converters (parse_types) for parse.
    It supports to build new type-converters for different cardinality
    based on the type-converter for cardinality one.
    """
    default_pattern = r".+?"

    @classmethod
    def with_cardinality(cls, cardinality, parse_type, listsep=','):
        if cardinality is Cardinality.one:
            return parse_type
        # -- NORMAL-CASE
        builder_func = getattr(cls, "with_%s" % cardinality.name)
        if cardinality is Cardinality.zero_or_one:
            return builder_func(parse_type)
        else:
            # -- MANY CASE: 0..*, 1..*
            return builder_func(parse_type, listsep=listsep)

    @classmethod
    def with_zero_or_one(cls, parse_type):
        """
        Creates a type-converter function for a T with 0..1 times
        by using the type-converter for one item of T.

        :param parse_type: Type-converter (function) for data type T.
        :return: type-converter for optional<T> (T or None).
        """
        def parse_optional(text, m=None):
            if text:
                text = text.strip()
            if not text:
                return None
            return parse_type(text)
        pattern = getattr(parse_type, "pattern", cls.default_pattern)
        new_pattern = Cardinality.zero_or_one.make_pattern(pattern)
        parse_optional.pattern = new_pattern
        return parse_optional

    @classmethod
    def with_zero_or_more(cls, parse_type, listsep=",", max_size=None):
        """
        Creates a type-converter function for a list<T> with 0..N items
        by using the type-converter for one item of T.

        :param parse_type: Type-converter (function) for data type T.
        :param listsep:  Optional list separator between items (default: ',')
        :param max_size: Optional max. number of items constraint (future).
        :return: type-converter for list<T>
        """
        def parse_list0(text, m=None):
            if text:
                text = text.strip()
            if not text:
                return []
            parts = [ parse_type(part.strip())
                      for part in text.split(listsep) ]
            return parts
        pattern  = getattr(parse_type, "pattern", cls.default_pattern)
        list_pattern = Cardinality.zero_or_more.make_pattern(pattern, listsep)
        parse_list0.pattern  = list_pattern
        parse_list0.max_size = max_size
        return parse_list0

    @classmethod
    def with_one_or_more(cls, parse_type, listsep=",", max_size=None):
        """
        Creates a type-converter function for a list<T> with 1..N items
        by using the type-converter for one item of T.

        :param parse_type: Type-converter (function) for data type T.
        :param listsep:  Optional list separator between items (default: ',')
        :param max_size: Optional max. number of items constraint (future).
        :return: type-converter for list<T>
        """
        def parse_list(text, m=None):
            parts = [ parse_type(part.strip())
                      for part in text.split(listsep) ]
            return parts
        pattern = getattr(parse_type, "pattern", cls.default_pattern)
        list_pattern = Cardinality.one_or_more.make_pattern(pattern, listsep)
        parse_list.pattern  = list_pattern
        parse_list.max_size = max_size
        return parse_list

    # -- ALIAS METHODS:
    @classmethod
    def with_optional(cls, parse_type):
        """Alias for :py:meth:`with_zero_or_one()` method."""
        return cls.with_zero_or_one(parse_type)

    @classmethod
    def with_many(cls, parse_type, **kwargs):
        """Alias for :py:meth:`with_one_or_more()` method."""
        return cls.with_one_or_more(parse_type, **kwargs)

    @classmethod
    def with_many0(cls, parse_type, **kwargs):
        """Alias for :py:meth:`with_zero_or_more()` method."""
        return cls.with_zero_or_more(parse_type, **kwargs)


    #@classmethod
    #def make_cardinality_variants(cls, parse_type, name=None,
    #                                    cardinalities=None, listsep=','):
    #    """
    #    Creates type variants for a parse_type with Cardinality.one.
    #    Uses the CardinalityField name convention for the created type variants:
    #
    #      * "Number"  (Cardinality.one)
    #      * "Number?" (Cardinality.zero_or_one = Cardinality.optional)
    #      * "Number*" (Cardinality.zero_or_more)
    #      * "Number+" (Cardinality.one_or_more = Cardinality.many)
    #
    #    .. code-block::
    #
    #        # Create all cardinality type variants for the type Number.
    #        # Creates: "Number?" (0..1), "Number*" (0..*), "Number+" (1..*)
    #        types = TypeBuilder.make_cardinality_variants(parse_number,
    #                        "Number", CardinalityField.pattern_chars)
    #        types = TypeBuilder.make_cardinality_variants(parse_number,
    #                        "Number", [Cardinality.optional, Cardinality.many])
    #
    #    :param parse_type:  Type converter for Cardinality.one.
    #    :param name:        Optional name (as string or None).
    #    :param cardinalities:  List of cardinalities or CardinalityField chars.
    #    :param listsep:     List separator to use (as string).
    #    :return: List of created parse_type variants.
    #    """
    #    assert callable(parse_type)
    #    if not name:
    #        name = parse_type.name
    #    if cardinalities is None:
    #        cardinalities = CardinalityField.pattern_chars
    #
    #    type_list = []
    #    for cardinality in cardinalities:
    #        if isinstance(cardinality, str):
    #            cardinality_char = cardinality
    #            cardinality = CardinalityField.from_char_map[cardinality_char]
    #        else:
    #            cardinality_char = CardinalityField.to_char_map[cardinality]
    #
    #        type_variant = cls.with_cardinality(cardinality, parse_type, listsep)
    #        type_variant.name = name + cardinality_char
    #        type_list.append(type_variant)
    #    return type_list

