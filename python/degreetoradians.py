#
#   --- SciLib ---
#

# define imports
import numpy as np
import re
from decimal import Decimal
from gmpy2 import const_pi      # mfr uses a wrapper function mpfr()


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
    
    # VALIDierung Min/Sek <60
    if minuten >= 60 or sekunden >= 60:
        return None
        
    return degree + minuten/60 + sekunden/3600


# function to convert from Degree to Radians     
def DegreeToRadians(x):
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
            print(f"mpfr input invalid: '{x}'. Use: mpfr('180.57') without symbols.")
            return None

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
                error_message = f"Invalid format: '{x}'.\nUse: 180.57, '180°', '180°20'', '180°20'13''', 2.3456e1 or mfpr('180.0')"
        
        else:
            error_message = "Input '{x}' must be numeric or valid string."
    
    except Exception as e:
        error_message = str(e)        
    
    if error_message:
        print(error_message)
        return None

            
# function to convert from Radians to Degree   
def RadiansToDegree(x):
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
                error_message = f"Invalid format: '{x}'.\nUse: radians 3.14, 1.234e1"
        
        else:
            error_message = "Input must be numeric or string."
    
    except Exception as e:
        error_message = str(e)
    
    if error_message:
        print(error_message)
        return None

# mpfr wraper function 
def mpfr(value, bit=128):
    import gmpy2 as mf
    try:
        s = float(value)
        s = mf.mpfr(value, bit)
    except Exception as e: 
        #print("nok: ", value)
        return value
    #print("ok: ", s)
    return s


# Usage examples
if __name__ == "__main__":
    print("Degree\n")
    result = DegreeToRadians("180")                 # will generate error, display the error
    if result is not None:                          # and provides a 'None' value 
        s = result * 34
    else:
        print("Calculation cannot be performed.\n")

    # More examples
    print(DegreeToRadians(180.57))                    # Decimal degrees example
    print(DegreeToRadians("180.57"))                  # Decimal degrees example
    print(DegreeToRadians("180°"))                    # DMS
    print(DegreeToRadians("180°40'13''"))             # DMS example
    print(DegreeToRadians("180°68'10''"))             # incorrect DMS example
    print(DegreeToRadians(2.3456e1))                  # Scientific notation example
    print(DegreeToRadians("2.3456e1"))                # Scientific notation example
    print(DegreeToRadians(mpfr("181.57")))            # mpfr decimal degrees example
    print(DegreeToRadians(mpfr("N 181.57")))          # incorrect mpfr decimal degrees example
    print(DegreeToRadians(mpfr("1.89°")))             # incorrect mpfr decimal degrees example
    
    print("Radians\n")

    print(RadiansToDegree(3.14))  
    print(RadiansToDegree("3.14"))  
    print(RadiansToDegree(np.pi))                     # π → 180° (mpfr)
    print(RadiansToDegree(mpfr('3.14159535', 128)))   # High precision
    print(RadiansToDegree("1.234e1"))                 # Scientific → Degrees
    print(RadiansToDegree("0.40938442"))              # DMS → Degrees (direct)

