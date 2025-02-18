# High Precision Float (HPF) Platform

<!--![HPF Logo](your-logo-url-here) <!-- Optional: Add a logo if available --> 

A pure Python implementation of a high-precision floating-point arithmetic class, designed to handle mathematical operations with enhanced precision beyond standard floating-point limitations.

## Features

- **High Precision**: Arbitrary precision arithmetic for both integer and fractional parts.
- **Multiple Initialization**: Supports initialization from `str`, `int`, and `float` types.
- **Operator Overloading**: Full support for `+`, `-`, `*`, `/`, `//`, and comparisons.
- **Negative Values**: Handles negative numbers with proper sign propagation.
- **Custom Precision**: Optional precision setting for division operations.
- **String Representation**: Clean string output with automatic trailing zero removal.

## Installation

### From PyPI

Using pip:
```bash
pip install hpf
```

### From Source

1. Use Source:

Simply include the `hpf.py` file in your project and import the class:

```python
from hpf import HighPrecisionFloat  # or 'from hpf import hpf, HPF(both OK)'
```

2. Compile Yourself:

There are 2 methods: 
 - Use setup.py
```bash
git clone https://github.com/zprolab/hpf
cd hpf 
pip install setuptools
setup.py install # Auto Install!
```
 - Use build (recommend)
```bash
git clone https://github.com/zprolab/hpf
cd hpf 
rm -rf ./dist
pip install setuptools build
python -m build # Auto Build!
pip install dist/*.whl
```

## Usage

### Test
```bash
python -m hpf
```

### Initialization
```python
from hpf import HighPrecisionFloat
```

### Abbreviations
```python
from hpf import HighPrecisionFloat as hpf
```
or
```python
from hpf import HighPrecisionFloat as HPF
```
or
```python
from hpf import hpf
```
or
```python
from hpf import HPF
```

```python
a = HighPrecisionFloat("3.14159265358979323846", precision=25)
b = HighPrecisionFloat(-42.75)
c = HighPrecisionFloat(1000)
```

### Basic Arithmetic
```python
x = HighPrecisionFloat("10.5")
y = HighPrecisionFloat("3.2")

print(x + y)  # 13.7
print(x - y)  # 7.3
print(x * y)  # 33.6
print(x / y)  # 3.28125
print(x // y) # 3
```

### Comparison Operations
```python
a = HighPrecisionFloat("100.001")
b = HighPrecisionFloat("100.002")

print(a < b)   # True
print(a == b)  # False
print(a >= b)  # False
```

### Sign Manipulation
```python
num = HighPrecisionFloat("-123.45")
num = -num  # Convert to positive
print(str(num)) # 123.45

num = +num  # Pos marking (no-op)
print(str(num))
```

### Precision Control
```python
# Set precision during initialization
div1 = HighPrecisionFloat("22", precision=50)
div2 = HighPrecisionFloat("7", precision=50)
print(str(div1/div2))
```

## Method Overview

### Core Methods
- `__init__`: Constructor with value parsing
- `_add_abs/_sub_abs`: Internal absolute addition/subtraction
- `_mul_abs/_div_abs`: Internal absolute multiplication/division
- `_abs_greater`: Absolute value comparison

### (TODO) Operator Overloads
- `+`, `-`, `*`, `/`, `//`
- `==`, `!=`, (TODO)`<`, (TODO)`<=`, (TODO)`>`, (TODO)`>=`

### Utility Methods
- `__str__/__repr__`: String representation
- `neg()/pos()`: Sign manipulation

## Considerations

1. **Performance**: Operations on very large numbers or high precision settings may impact performance.
2. **Division Precision**: The `precision` parameter in division defaults to 10 decimal places. Increase this for more precise results.
3. **Zero Handling**: Trailing fractional zeros are automatically removed in string representation.

## License
MIT License - See [LICENSE](LICENSE) file for details.

## Author
Chenyun Z. 
Created: Oct 27 2024  
Last Updated: Feb 18 2025

## Something...
PyPI is a great invention to make package-managing easier!

GitHub Action is also a great invention to let we needn't to write `python -m build` again and again!
