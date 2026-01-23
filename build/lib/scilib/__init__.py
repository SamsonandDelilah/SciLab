# __init__.py 
from .config import config
from .convert_angle_units import deg_to_rad, rad_to_deg

__all__ = ["deg_to_rad", "rad_to_deg", "config"]  
__version__ = "0.1.0"

# Comments
# Namespace Access:
# config.errors.mode = "silent"
# config.si.length_unit = "km" # tbd
# config.precision.digits = 128          # e.g. for mpfr settings

