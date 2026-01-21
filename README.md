```markdown
# SciLib - Precision Angle Conversion Library

**Unified SOT conversion for ALL input formats with automatic validation!**

## 🚀 Motivation

**Problem:** Every library handles angle systems differently:
```
numpy.deg2rad("180°20'")     → Error
math.radians("180.57grad")   → Error  
scipy.invalid_input("2g")    → Error
```

**SciLib solves it:** **1 API → all formats** with precision checking!

## 📦 Installation

```bash
pip install git+https://github.com/SamsonandDelilah/SciLab.git#subdirectory=python
```

## 💻 Usage

```python
from scilib import GradToRadians, RadiansToGrad

# Safe usage with validation
result = GradToRadians("180")
if result is not None:
    s = result * 34
else:
    print("Calculation cannot be performed.")

# Broad format spectrum
print(GradToRadians(180.57))                    # Decimal degrees
print(GradToRadians("180°20'13''"))             # DMS
print(GradToRadians("2.3456e1"))                # Scientific
print(GradToRadians(mpfr("180.57")))           # High-Precision

print("\nRadians → Degrees:")
print(RadiansToGrad(np.pi))                     # π → 180°
print(RadiansToGrad(mpfr('3.1415926535', 128))) # 128-bit
print(RadiansToGrad("1.234e1"))                 # Scientific
```

## 🎯 Supported Formats

| Type | Examples |
|------|----------|
| Decimal | `180.57`, `"180.57grad"` |
| DMS | `"180°20'13''"`, `"N 48°12'30''"` |
| Scientific | `"1.234e2"`, `"2.3456E1grad"` |
| High-Precision | `mpfr("3.14159", 256)` |

## 🛠 Roadmap

```
SciLab (Monorepo)
├── python/     → pip install scilib
├── rust/       → cargo add scilib
└── cpp/        → #include <scilib-cpp>
```

## 🤝 Feedback Welcome!

https://github.com/SamsonandDelilah/SciLab/issues

**For 3D Graphics, Physics, Astronomy and more!** ⭐
```

**Perfect professional English README!** 🚀