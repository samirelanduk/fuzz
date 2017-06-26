fuzz
====

fuzz is a lightweight Python utility providing values with associated
uncertainty.

Example
-------

  >>> import fuzz
  >>> value1 = fuzz.Value(23, error=0.3)
  >>> value2 = fuzz.Value(28, error=1.3)
  >>> value1
  23 ± 0.3
  >>> value2
  28 ± 1.3
  >>> value1 + value2
  51 ± 1.3341664064126335


Table of Contents
-----------------

.. toctree ::

    installing
    changelog
