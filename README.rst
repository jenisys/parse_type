===============================================================================
parse_type
===============================================================================

.. image:: https://pypip.in/v/parse_type/badge.png
    :target: https://crate.io/packages/parse_type/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/parse_type/badge.png
    :target: https://crate.io/packages/parse_type/
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/jenisys/parse_type.png?branch=master
    :target: https://travis-ci.org/jenisys/parse_type
    :alt: Travis CI Build Status


`parse_type`_ extends the `parse`_ module (opposite of `string.format()`_)
with the following features:

    * build parse_types for common use cases (enum/mapping, choice)
    * build a parse_type with a cardinality constraint (0..1, 0..*, 1..*)
      from the parse_type for cardinality=1.
    * compose parse types from other parse types


.. _parse_type: http://pypi.python.org/pypi/parse_type
.. _parse:      http://pypi.python.org/pypi/parse
.. _`string.format()`: http://docs.python.org/library/string.html#format-string-syntax


CONCEPTS
-------------------------------------------------------------------------------

type converter:

    A type converter function that converts a textual representation
    of a value type into instance of this value type.

parse_type:

    A type converter function that is annotated with attributes
    that allows the `parse`_ module to process it as generic type.


Basic Example
-------------------------------------------------------------------------------

Define an own parse_type for numbers (integers):

.. code-block:: python

    # -- USE CASE:
    def parse_number(text):
        return int(text)
    parse_number.pattern = r"\d+"  # -- REGULAR EXPRESSION pattern for type.

This is equivalent to:

.. code-block:: python

    import parse

    @parse.with_pattern(r"\d+")
    def parse_number(text):
         return int(text)
    assert hasattr(parse_number, "pattern")
    assert parse_number.pattern == r"\d+"


.. code-block:: python

    # -- USE CASE: Use the parse_type (type converter).
    schema = "Hello {number:Number}"
    parser = parse.Parser(schema, dict(Number=parse_number))
    result = parser.parse("Hello 42")
    assert result is not None, "REQUIRE: text matches the schema."
    assert result.number == 42

    result = parser.parse("Hello XXX")
    assert result is None, "MISMATCH: text does not match the schema."


Cardinality
-------------------------------------------------------------------------------

.. code-block:: python

    # -- USE CASE: Create new parse_type with a cardinality constraint.
    # CARDINALITY: many := one or more (1..*)
    from parse import Parser
    from parse_type import TypeBuilder
    parse_numbers = TypeBuilder.with_many(parse_number, listsep=",")

    schema = "List: {numbers:ManyNumbers}"
    parser = Parser(schema, dict(ManyNumbers=parse_numbers))
    result = parser.parse("List: 1, 2, 3")
    assert result.numbers == [1, 2, 3]

.. code-block:: python

    # -- USE CASE: Create new parse_type with cardinality constraint.
    # CARDINALITY: optional := zero or one (0..1)
    from parse import Parser
    from parse_type import TypeBuilder

    parse_optional_number = TypeBuilder.with_optional(parse_number)
    schema = "Optional: {number:OptionalNumber}"
    parser = Parser(schema, dict(OptionalNumber=parse_optional_number))
    result = parser.parse("Optional: 42")
    assert result.number == 42
    result = parser.parse("Optional: ")
    assert result.number == None


Enumeration (Name-to-Value Mapping)
-------------------------------------------------------------------------------

.. code-block:: python

    # -- USE CASE: Create an enumeration parse_type (name-to-value mapping).
    from parse import Parser
    from parse_type import TypeBuilder

    parse_enum_yesno = TypeBuilder.make_enum({"yes": True, "no": False})
    parser = Parser("Answer: {answer:YesNo}", dict(YesNo=parse_enum_yesno))
    result = parser.parse("Answer: yes")
    assert result.answer == True


.. code-block:: python

    # -- USE CASE: Create a parse_type for enum34 enumeration class.
    # NOTE: Use Python 3.4 or enum34 backport.
    from parse import Parser
    from parse_type import TypeBuilder
    from enum import Enum

    class Color(Enum):
        red   = 1
        green = 2
        blue  = 3

    parse_enum_color = TypeBuilder.make_enum(Color)
    parser = Parser("Select: {color:Color}", dict(Color=parse_enum_color))
    result = parser.parse("Select: red")
    assert result.color is Color.red


Choice (Name Enumeration)
-------------------------------------------------------------------------------

A Choice data type allows to select one of several strings.

.. code-block:: python

    from parse import Parser
    from parse_type import TypeBuilder

    parse_choice_yesno = TypeBuilder.make_choice(["yes", "no"])
    schema = "Answer: {answer:ChoiceYesNo}"
    parser = Parser(schema, dict(ChoiceYesNo=parse_choice_yesno))
    result = parser.parse("Answer: yes")
    assert result.answer == "yes"
