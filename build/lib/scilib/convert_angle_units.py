#
#   --- degree_to_radians and vice versa ---
#

# Global GMPY2 state
GMPY2_AVAILABLE = False

try:
    from gmpy2 import const_pi, mpfr
    GMPY2_AVAILABLE = True
except ImportError:
    # Graceful fallback für basic users
    const_pi = 3.141592653589793
    def mpfr(value, bits=128):
        return float(value)
    
# degree_to_radians.py - DEV ONLY
try:
    from scilib.config import config
except ImportError:
    from config import config  # local dev name
    
# define imports
import numpy as np
import re
from decimal import Decimal
from gmpy2 import const_pi      # mfr uses a wrapper function mpfr()
#from config import config
import logging

config.errors.mode = "silent"       # silent, warn, strict
logger = logging.getLogger("scilib")

# helper function for DMS
def parse_flexible_dms(dms_string):
    """
    Parse flexible DMS format: "180°", "180°20'", "180°20'13''"
    Prüft Minuten <60, Sekunden <60. Returns decimal degrees oder None.
    """
    flexible_dms = r"^(-?\d+)(°(?:\s*(\d{1,2})'?(?:\s*(\d{1,2})''?)?)?)?$"
    match = re.match(flexible_dms, dms_string.strip())
    
    if not match:
        return None
    
    degree = int(match.group(1))
    minuten = int(match.group(3)) if match.group(3) else 0
    sekunden = int(match.group(4)) if match.group(4) else 0
    
    # validation Min/Sec <60
    if minuten >= 60 or sekunden >= 60:
        return None
        
    return degree + minuten/60 + sekunden/3600


# function to convert from Degree to Radians     
def deg_to_rad(x):
    """
    Converts angle inputs to radians.

    Supported input formats:
    - Decimal degrees (float, int, Decimal, BigFloat)
    - Flexible DMS: "180°", "180°20'", "180°20'13''"
    - Decimal/scientific strings: "180.57", "2.3456e1" or mpfr('180.001')

    :param x: Angle to convert. Numeric or string.
    :return: Radians (mpfr) or None on error.
    """
    x = mpfr(x)
    import gmpy2 as mf
    error_message = None
    
    if isinstance(x, mf.mpfr):
        x_str = str(x)
        if any(symbol in x_str for symbol in ['°', "'", '"', "'"]):
            config.handle_error(f"mpfr input contains DMS symbols: {x}")

    try:

        # Numeric input
        if isinstance(x, (int, float, Decimal, mf.mpfr)):
            if isinstance(x, mf.mpfr):
                x_str = str(x)
                if '°' in x_str:
                    raise ValueError(f"mpfr cannot parse degree symbol: {x_str}")
                decimal_value = x
            elif isinstance(x, Decimal):
                decimal_value = mf.mpfr(str(x))
            else:
                decimal_value = mf.mpfr(x)
            return decimal_value * const_pi() / mf.mpfr('180')

        # String input
        elif isinstance(x, str):
            # 1. Flexible DMS
            dms_decimal = parse_flexible_dms(x)
            if dms_decimal is not None:
                return mf.mpfr(dms_decimal) * const_pi() / mf.mpfr('180')
            
            # 2. Decimal: "180.57"
            decimal_pattern = r"^(-?\d+(?:\.\d+)?)$"
            # 3. Scientific: "2.3456e1"
            scientific_pattern = r"^(-?\d+(?:\.\d+)?[eE][+-]?\d+)$"
            
            match_decimal = re.match(decimal_pattern, x)
            match_scientific = re.match(scientific_pattern, x)
            
            if match_decimal or match_scientific:
                return mf.mpfr(x) * const_pi() / mf.mpfr('180')
            
            else:
                return config.handle_error(
                    f"Invalid format: '{x}'.\n"
                    "Use one of: 180.57, '180°', '180°20'', '180°20'13''', 2.3456e1, mpfr('180.0')"
                )

        
        else:
            return config.handle_error("Input '{x}' must be numeric or valid string.")
    
    except Exception as e:
        return config.handle_error(f"Conversion failed: {str(e)}")


            
# function to convert from Radians to Degree   
def rad_to_deg(x):
    """
    Converts radians to degrees or parses DMS to decimal degrees.
    
    Supported formats:
    - Radians (float, int, Decimal, mpfr)
    - Flexible DMS: "180°", "180°20'", "180°20'13''"
    - Decimal/scientific strings → radians → degrees

    :param x: Angle in radians or DMS string.
    :return: Degrees (mpfr) or None on error.
    """
    x = mpfr(x)
    import gmpy2 as mf
    error_message = None
    try:
        # Numeric input (radians)
        if isinstance(x, (int, float, Decimal, mf.mpfr)):
            if isinstance(x, mf.mpfr):
                radian_value = x
            elif isinstance(x, Decimal):
                radian_value = mf.mpfr(str(x))
            else:
                radian_value = mf.mpfr(x)
            return radian_value * mf.mpfr('180') / const_pi()

        # String input
        elif isinstance(x, str):
            # 1. Flexible DMS → direkt Degrees
            dms_decimal = parse_flexible_dms(x)
            if dms_decimal is not None:
                return mf.mpfr(dms_decimal)
            
            # 2. Decimal/Scientific → radians → degrees
            decimal_pattern = r"^(-?\d+(?:\.\d+)?)$"
            scientific_pattern = r"^(-?\d+(?:\.\d+)?[eE][+-]?\d+)$"
            
            match_decimal = re.match(decimal_pattern, x)
            match_scientific = re.match(scientific_pattern, x)
            
            if match_decimal or match_scientific:
                return mf.mpfr(x) * mf.mpfr('180') / const_pi()
            
            else:
                config.handle_error(f"Invalid format: '{x}'.\nUse: radians 3.14, 1.234e1")
        
        else:
            config.handle_error("Input must be numeric or string.")
    
    except Exception as e:
        return config.handle_error(f"Conversion failed: {str(e)}")


# mpfr wraper function 
def mpfr(value, bit=128):
    """Safe mpfr wrapper - float check first."""
    try:
        import gmpy2 as mf
        
        # 1. Float-Test blockiert "180°" → handle_error → None ✓
        _ = float(value)  
        
        # 2. mpfr nur bei gültigem Float
        return mf.mpfr(str(value), bit)
        
    except Exception:
        # Dein Fallback!
        return config.handle_error(
            f"mpfr conversion failed for '{value}'"
        ) or value  # Fallback zu Original



# Usage examples
if __name__ == "__main__":
    print("Degree\n")
    result = deg_to_rad("180")                   # will generate error, display the error
    if result is not None:                          # and provides a 'None' value 
        s = result * 34
    else:
        print("Calculation cannot be performed.\n")

    # More examples
    print(deg_to_rad(180.57))                       # Decimal degrees example
    print(deg_to_rad("180.57"))                     # Decimal degrees example
    print(deg_to_rad("180°"))                       # DMS
    print(deg_to_rad("180°40'13''"))                # DMS example
    print(deg_to_rad("180°68'10''"))                # incorrect DMS example
    print(deg_to_rad(2.3456e1))                     # Scientific notation example
    print(deg_to_rad("2.3456e1"))                   # Scientific notation example
    print(deg_to_rad(mpfr("181.57")))               # mpfr decimal degrees example
    print(deg_to_rad(mpfr("N 181.57")))             # incorrect mpfr decimal degrees example
    print(deg_to_rad(mpfr("1.89°")))                # incorrect mpfr decimal degrees example
    
    print("Radians\n")

    print(rad_to_deg(3.14))  
    print(rad_to_deg("3.14"))  
    print(rad_to_deg(np.pi))                     # π → 180° (mpfr)
    print(rad_to_deg(mpfr('3.14159535', 128)))   # High precision
    print(rad_to_deg("1.234e1"))                 # Scientific → Degrees
    print(rad_to_deg("0.40938442"))              # DMS → Degrees (direct)

