Overview
--------

fuzz allows you to manipulate numbers which are the result of a measurement, and
which therefore have uncertainty bounds associated with them.

All methods of measuring a physical quantity - reading a thermometer, weighing
yourself, measuring the speed of a car - produce values which are actually
'plus or minus' some amount, because all methods of measurement have limits to
their precision. It is this 'plus or minus' which fuzz handles.

Creating
~~~~~~~~

The key (and currently only) object type in fuzz is the :py:class:`.Value`. A
Value is just a number, or measurement. The most basic Value would be created
as follows:

    >>> from fuzz import Value
    >>> val = Value(108.5)
    >>> val
    108.5
    >>> type(val)
    <class 'fuzz.values.Value'>

Here a Value is created to represent the number of 108.5. There is no error
associated (error and uncertainty are used interchangeably here), and it is
generally indistinguishable from the ``float`` 108.5, unless you actually query
its type.

You would add error like this:

    >>> val = Value(108.5, 1.4)
    >>> val
    108.5 ± 1.4
    >>> val.value()
    108.5
    >>> val.error()
    1.4

This represents a value of 108.5, but for which there is uncertainty in either
direction of 1.4 - '108.5 plus or minus 1.4'. This error can be represented in
other ways:

    >>> val.relative_error() # The error relative to the value
    0.012903225806451613
    >>> val.error_range() # The range of possible values implied by the error
    (107.1, 109.9)


Mathematical Operations
~~~~~~~~~~~~~~~~~~~~~~~

Values can be added, subtracted, multiplied, and divided - with other Values and
with ordinary numbers. The result will be a new Value, whose value is the result
of that operation.

    >>> val1 = (96, 1.5)
    >>> val2 = (23, 0.8)
    >>> sum_val = val1 + val2
    >>> sum_val.value()
    119
    >>> product_val = val1 * val2
    product_val.value()
    2208

The new Value will also have an error associated, that comes from the error
values of the operands. The values are assumed to be independent, and so error
values are combined
`in quadrature <http://ipl.physics.harvard.edu/wp-uploads/2013/03/PS3_Error_Propagation_sp13.pdf>`_

You can also raise a Value to a power.

Comparing
~~~~~~~~~

Values support the ``==``, ``!=``, ``<``, ``<=``, ``>`` and ``>=`` comparison
operators. These will just compare the values themselves, and ignore error.

However, the error is important when comparing uncertain values. The expression
``Value(10, 5) > Value(9, 4)`` will return ``True``, because 10 is greater than
9. But mathematically, the values are so uncertain and so close, that you might
wish to check that this difference is significant.

For this purpose, the :py:meth:`~.Value.consistent_with` method can be used.
Two values are consistent if the sum of their errors is larger than the
difference between their values. ``Value(10, 5).consistent_with(Value(9, 4))``
would return ``True``, and so whatever the operands might say, you should be
careful about treating one as being unambiguously larger than the other.
