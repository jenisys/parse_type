# -*- coding: utf-8 -*-
"""
Provides support to compose user-defined parse types.

Cardinality
------------

It is often useful to constrain how often a data type occurs.
This is also called the cardinality of a data type (in a context).
The supported cardinality are:

  * 0..1  zero_or_one,  optional<T>: T or None
  * 0..N  zero_or_more, list_of<T>
  * 1..N  one_or_more,  list_of<T> (many)

.. code-block:: python

    >>> from parse_type import TypeBuilder
    >>> from parse import Parser

    >>> def parse_number(text):
    ...     return int(text)
    >>> parse_number.pattern = r"\d+"

    >>> parse_many_numbers = TypeBuilder.with_many(parse_number)
    >>> more_types = { "Numbers": parse_many_numbers }
    >>> parser = Parser("List: {numbers:Numbers}", more_types)
    >>> parser.parse("List: 1, 2, 3")
    <Result () {'numbers': [1, 2, 3]}>


Enumeration Type (Name-to-Value Mappings)
-----------------------------------------

An Enumeration data type allows to select one of several enum values by using
its name. The converter function returns the selected enum value.

.. code-block:: python

    >>> from parse_type import TypeBuilder
    >>> from parse import Parser

    >>> parse_enum_yesno = TypeBuilder.make_enum({"yes": True, "no": False})
    >>> more_types = { "YesNo": parse_enum_yesno }
    >>> parser = Parser("Answer: {answer:YesNo}", more_types)
    >>> parser.parse("Answer: yes")
    <Result () {'answer': True}>


Choice (Name Enumerations)
-----------------------------

A Choice data type allows to select one of several strings.

EXAMPLE:

    >>> parse_choice_yesno = TypeBuilder.make_choice(["yes", "no"])
    >>> more_types = { "ChoiceYesNo": parse_choice_yesno }
    >>> parser = Parser("Answer: {answer:ChoiceYesNo}", more_types)
    >>> parser.parse("Answer: yes")
    <Result () {'answer': 'yes'}>

"""

from __future__ import absolute_import
from .cardinality import TypeBuilder as CardinalityTypeBuilder
import enum
import inspect

__all__ = ["TypeBuilder", "build_type_dict"]


class TypeBuilder(CardinalityTypeBuilder):
    """
    Provides a utility class to build type-converters (parse_types) for
    the :mod:`parse` module.
    """
    default_pattern = r".+?"
    default_strict = True

    @staticmethod
    def make_enum(enum_mappings):
        """
        Create a type-converter function object for this enumeration.

        :param enum_mappings: Defines enumeration names and values.
        :return: Type-converter (parse_enum) function object.
        """
        if (inspect.isclass(enum_mappings) and
            issubclass(enum_mappings, enum.Enum)):
            enum_class = enum_mappings
            enum_mappings = enum_class.__members__

        def parse_enum(text):
            if text not in parse_enum.mappings:
                text = text.lower()     # REQUIRED-BY: parse re.IGNORECASE
            return parse_enum.mappings[text]    #< text.lower() ???
        parse_enum.pattern = r"|".join(enum_mappings.keys())
        parse_enum.mappings = enum_mappings
        return parse_enum

    @staticmethod
    def _normalize_choices(choices, transform):
        assert transform is None or callable(transform)
        if transform:
            choices = [transform(value)  for value in choices]
        else:
            choices = list(choices)
        return choices

    @classmethod
    def make_choice(cls, choices, transform=None, strict=None):
        """
        Creates a type-converter function to select one from a list of strings.
        The type-converter function returns the selected choice_text.
        The :param:`transform()` function is applied in the type converter.
        It can be used to enforce the case (because parser uses re.IGNORECASE).

        :param choices: List of strings as choice.
        :param transform: Optional, initial transform function for parsed text.
        :return: Type-converter (parse_choice) function object.
        """
        # -- NOTE: Parser uses re.IGNORECASE flag
        #    => transform may enforce case.
        choices = cls._normalize_choices(choices, transform)
        if strict is None:
            strict = cls.default_strict

        def parse_choice(text):
            if transform:
                text = transform(text)
            if strict and not (text in parse_choice.choices):
                values = ", ".join(parse_choice.choices)
                raise ValueError("%s not in: %s" % (text, values))
            return text
        parse_choice.pattern = r"|".join(choices)
        parse_choice.choices = choices
        return parse_choice

    @classmethod
    def make_choice2(cls, choices, transform=None, strict=None):
        """
        Creates a type-converter function to select one from a list of strings.
        The type-converter function returns a tuple (index, choice_text).

        :param choices: List of strings as choice.
        :param transform: Optional, initial transform function for parsed text.
        :return: Type-converter (parse_choice) function object.
        """
        choices = cls._normalize_choices(choices, transform)
        if strict is None:
            strict = cls.default_strict

        def parse_choice2(text):
            if transform:
                text = transform(text)
            if strict and not (text in parse_choice2.choices):
                values = ", ".join(parse_choice2.choices)
                raise ValueError("%s not in: %s" % (text, values))
            # XXX-JE-UNCLEAR-WHY-NEEDED:
            #if not text:
            #    return None #< OPTIONAL CASE OCCURED.
            index = parse_choice2.choices.index(text)
            return index, text
        parse_choice2.pattern = r"|".join(choices)
        parse_choice2.choices = choices
        return parse_choice2

# -- IDEA:
#    @classmethod
#    def make_type_choice(cls, type_converters):
#        """
#        Creates a type-converter function for several converter alternatives.
#
#        :param type_converters: List of type-converter alternatives.
#        :return: Type-converter function object.
#        """
#        needs_default_pattern = 0
#        choice_patterns = []
#        for type_converter in type_converters:
#            pattern = getattr(type_converter, "pattern", None)
#            if not pattern:
#                needs_default_pattern += 1
#                continue
#            choice_patterns.append(pattern)
#        if needs_default_pattern:
#            assert needs_default_pattern == 1
#            choice_patterns.append(cls.default_pattern)
#
#        def parse_type_choice(text):
#            # NEED TO KNOW: Which type converter pattern was matched.
#            # return parse_type_choice.converters[x](text)
#            return text
#
#        parse_type_choice.pattern = r"|".join(choice_patterns)
#        parse_type_choice.converters = type_converters
#        return parse_type_choice


def build_type_dict(type_converters):
    """
    Builds type dictionary for user-defined type converters,
    used by :mod:`parse` module.
    This requires that each type converter has a "name" attribute.

    :param type_converters: List of type-converters (parse_types)
    :return: Type-converter dictionary
    """
    more_types = {}
    for type_converter in type_converters:
        assert callable(type_converter)
        more_types[type_converter.name] = type_converter
    return more_types


# -- AUTO-MAIN:
if __name__ == "__main__":
    import doctest
    doctest.testmod()

# -----------------------------------------------------------------------------
# Copyright (c) 2012 by Jens Engel (https://github/jenisys/)
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