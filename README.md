## SciLib - High-Precision Scientific Library
**Unified single Source-of-Truth (SOT) conversion for ALL input formats with automatic validation!**

Contents:
1. Angle Conversion convert_angle_units.py (deg_to_rad, rad_to_deg, config)

## 🚀 Motivation ##

**Problem:** Every library handles angle systems differently:

| Library | Example | Result |
|---------|----------|----------|
| numpy   | `np.deg2rad("180°20'")` | ❌ Error |
| math    | `math.radians("180.57degree")` | ❌ Error |
| scipy   | `scipy.invalid_input("2g")` | ❌ Error |
| **scilib** | `deg_to_rad("180°20'")` | ✅ 3.1415... |



**SciLib solves it:** **1 API → all formats** with precision checking!

## 💻 Usage ##

```python
# 1. Namespace Import (recommended)
from scilib import deg_to_rad, rad_to_deg, config # Warning: mpfr is a wrapper of mpfr in convert_angle_units()

# 2. Direct Module Import  
#from scilib.convert_angle_units import deg_to_rad

config.errors.mode = "silent"                     # silent, warn, strict
logger = logging.getLogger("scilib")

# Safe usage with validation
result = deg_to_rad("N 180°")                     # ❌ will display Error and provides a 'None' value
if result is not None:                            
    s = result * 34
else:
    print("Calculation cannot be performed.")

# Broad format spectrum
print("\nDegrees → Radians:")
print(deg_to_rad(180.57))                         # Decimal degrees example
print(deg_to_rad("180.57"))                       # Decimal degrees example
print(deg_to_rad("180°"))                         # DMS
print(deg_to_rad("180°40'13''"))                  # DMS example
print(deg_to_rad("180°68'10''"))                  # incorrect DMS example
print(deg_to_rad(2.3456e1))                       # Scientific notation example
print(deg_to_rad("2.3456e1"))                     # Scientific notation example
print(deg_to_rad(mpfr("181.57")))                 # mpfr decimal degrees example, Warning: mpfr is a wrapper in convert_degree_to_radians()
print(deg_to_rad(mpfr("N 181.57")))               # ❌ will display Error, incorrect mpfr string format 
print(deg_to_rad(mpfr("1.89°")))                  # ❌ will display Error, incorrect mpfr string format 

print("\nRadians → Degrees:")
print(rad_to_deg(3.14))  
print(rad_to_deg("3.14"))  
print(rad_to_deg(np.pi))                          # π → 180° (mpfr)
print(rad_to_deg(mpfr('3.14159535', 128)))        # High precision
print(rad_to_deg("1.234e1"))                      # Scientific → Degrees
print(rad_to_deg("0.40938442"))                   # DMS → Degrees (direct)
```

## 🎯 Supported Formats

| Type | Examples |
|------|----------|
| Decimal degree | `180.57` |
| DMS | `"180°20'13''"`  |
| Scientific | `"1.234e2"` |
| High-Precision | `mpfr("3.14159", 256)` |

> **⚠️ Warning**: `mpfr()` is an internal wrapper of `gmpy2.mpfr()` in `convert_angle_units.py`. External `gmpy2` installation optional.
Supported types are integer, float, decimal and Arbitrary Precision with `gmpy2.mpfr()` string format.

## 🛠 Roadmap

```
SciLib (Monorepo)
├── python/     → pip install scilib
├── rust/       → cargo add scilib
└── cpp/        → #include <scilib-cpp>
```

It is intended to expand this SciLib continously (fully supporting a simple SOT approach only), help is welcome.
Next steps:
- inlcude rad, gon, milrad, mil
- setup data concept for SciLib

## 📦 Installation

```Powershel or bash
pip install git+https://github.com/SamsonandDelilah/SciLib.git#subdirectory=python
```


## 🤝 Feedback Welcome!

I would love to hear from you, what you think about or how I can help or how you possible would like to help me.

https://github.com/SamsonandDelilah/SciLib/issues

## Licensing

Scilib is released under the [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/SamsonandDelilah/SciLib/blob/main/LICENSE) license.

**For 3D Graphics, Physics, Astronomy and more!** ⭐

