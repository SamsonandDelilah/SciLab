"""SciLib Configuration - Single Source of Truth."""
import logging
from typing import Any
from enum import Enum
from pathlib import Path
import json
import os
from pathlib import Path
from importlib import resources
constants_path = resources.files(__package__) / "data" / "constants"

# Logger setup
logger = logging.getLogger("scilib")


def _get_data_path():
    from pathlib import Path  # ← HIER FEHLT!
    import os, site
    
    try:
        # 1. Package data (Python 3.9+)
        from importlib.resources import files
        data_path = files('scilib') / 'data'
        if data_path.exists():
            return data_path
    except:
        pass
    
    # 2. Dev fallback: relative zum Projekt root
    return Path(__file__).parent.parent.parent / 'data'  # ROOT/data/

class ErrorMode(Enum):
    STRICT = "strict"      # raise alle Exceptions
    WARN = "warn"          # log warnings, return None  
    SILENT = "silent"      # nur None, keine Logs

class ErrorsConfig:
    def __init__(self):
        self._mode = ErrorMode.STRICT  # Default
        self.log_level = "WARNING"
    
    @property
    def mode(self):
        return self._mode
    
    @mode.setter
    def mode(self, value):
        self._mode = ErrorMode(value) if isinstance(value, str) else value
    
    @property
    def silent(self):
        return self._mode == ErrorMode.SILENT
    
    @property
    def raise_exceptions(self):
        return self._mode == ErrorMode.STRICT

class SISystemConfig:
    """SI Unit System configuration."""
    length_unit = "m"
    pressure_unit = "Pa"

class PrecisionConfig:
    """Set numerical precision for mathematical calculations."""
    digits = 20
    bits = 128  

class ConstantsConfig:
    """Constants subsystem configuration"""
    def __init__(self):
        self.version = "CODATA2022"
        
class Config:
    """Lists all available config handlers"""
    def __init__(self):
        self.errors = ErrorsConfig()
        self.si = SISystemConfig()
        self.precision = PrecisionConfig()
        self.constants = ConstantsConfig() 

        @property
        def constants_version(self):
            return self.constants.version
        
        @constants_version.setter
        def constants_version(self, version):
            self.constants.version = version
            
    def physical_constants(self, name, version=None):
        """SciPy-kompatibel: ('speed of light') → (value, unit, unc)"""
        if version is None:
            version = self.constants.version
        
        data_path = _get_data_path()
        
        # Versioned first
        versioned_path = data_path / f"constants/{version}/{name}.json"
        if versioned_path.exists():
            data = json.loads(versioned_path.read_text())
            return data["value"], data["unit"], data["uncertainty"]
        
        # Latest fallback
        latest_path = data_path / f"constants/{name}.json"
        if latest_path.exists():
            data = json.loads(latest_path.read_text())
            return data["value"], data["unit"], data["uncertainty"]
        
        # ← SCI-LIB STYLE!
        self.handle_error(f"Constant '{name}' not found in {data_path}")
        return None  # SILENT fallback
    
        
    def handle_error(self, msg: str) -> Any:
        """Unified error handling across SciLib."""
        mode = self.errors.mode
        if mode == ErrorMode.STRICT:
            raise ValueError(msg)
        elif mode == ErrorMode.WARN:
            logger.warning(msg)
        elif mode == ErrorMode.SILENT:  
            logger.debug(msg)  # Still logged, but no user impact
        return None # SILENT
    
    

# Global instance
config = Config()


"""
# Nutzung:
config.errors.mode = "silent"     # 1 Zeile!
r = deg_to_rad("invalid")         # → None

config.errors.mode = "warn"       # Logs + None
"""