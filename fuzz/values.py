"""Contains the Value class."""

class Value:
    """A Value represents a numerical measurement of some kind, with its
    associated uncertainty/error.

    For example a value of 23 ± 0.2 would be ``Value(23, 0.2)``

    Values mostly support the same operators that numbers do - you can add them,
    divide them, raise them to powers, compare them etc. There are a few
    important differences however. Firstly, the error values of the resultant
    operations will be derived from the standard guidelines for combining
    uncertainties. That is, adding two values will sum their errors, as will
    subtracting. Multiplying and dividing values will sum the relative errors.
    Secondly, comparing two values with ``==``, ``<`` etc. will compare the
    values only - the error values will not be taken into account. I thought it
    would be too confusing otherwise. However, all values have a
    :py:methh:`.consistent_with` method which `will` look at the error values.
    If two values are consistent, then one should not be considered larger than
    the other, regardless of what ``>`` says.

    :param value: The value.
    :param error: The uncertainty associated with the value. By default this is\
    zero.
    :raises TypeError: if either the value or its error is not numeric.
    :raises ValueError: if the error is negative."""

    def __init__(self, value, error=0):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return TypeError("value {} is not an int or a float".format(value))
        if not isinstance(error, (int, float)) or isinstance(error, bool):
            return TypeError("error {} is not an int or a float".format(error))
        if error < 0:
            raise ValueError("error {} is negative".format(error))
        self._value = value
        self._error = error
