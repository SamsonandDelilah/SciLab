# SciLib - High-Precision Scientific Library (Monorepo)

**Single Source-of-Truth (SOT) für Physics, Astronomy, 3D Graphics**

## 🚀 Languages

| Language | Status | Install | Import |
|----------|--------|---------|--------|
| 🐍 Python | ✅ Live | `pip install scilib` | `from scilib import deg_to_rad` |
| 🦀 Rust | ⏳ Coming soon | `cargo add scilib` | `use scilib::deg_to_rad;` |
| ⚡ C++ | ⏳ Coming soon | `vcpkg install scilib` | `#include <scilib/angle.hpp>` |

## 📦 Quickstart Python
```bash
pip install git+https://github.com/SamsonandDelilah/SciLib.git#subdirectory=python
python -c "from scilib import deg_to_rad; print(deg_to_rad('180°'))"
