"""SciLib Configuration - Single Source of Truth."""
import logging
from typing import Any
from enum import Enum
from pathlib import Path
import json
import os
import io
import zipfile
import requests
from pathlib import Path
from urllib.parse import urljoin

# Logger setup
logger = logging.getLogger("scilib")


def ensure_data():
    """Auto-download SciLib data bei erstem Lauf"""
    data_dir = Path.home() / ".scilib" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    json_path = data_dir / "constants" / "speed_of_light.json"
    if not json_path.exists():
        print("📥 Downloading SciLib data (first run)...")
        
        # GitHub Releases (automatisch latest)
        repo_url = "https://github.com/SamsonandDelilah/SciLib"
        api_url = f"{repo_url}/releases/latest"
        release = requests.get(api_url).json()
        
        # Finde data.zip asset
        data_asset = next((a for a in release['assets'] if 'data' in a['name'].lower()), None)
        if not data_asset:
            raise RuntimeError("data.zip not found in latest release. Please check GitHub.")
        
        print(f"  ↓ {data_asset['name']} ({data_asset['size']/1e6:.1f} MB)")
        zip_content = requests.get(data_asset['browser_download_url']).content
        
        # Extract
        with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
            z.extractall(data_dir)
        
        print("✅ SciLib data ready! (~/.scilib/data/)")
    
    return data_dir

def _get_data_path():
    """Data path mit auto-download"""
    data_dir = os.getenv('SCILIB_DATA')
    if data_dir:
        return Path(data_dir)
    
    return ensure_data()


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
        """Lazy load: default → cache hit, versioned → on-demand"""
        if version is None:
            version = self.constants.version  # CODATA2022 default
            
        # Cache check (schnell!)
        cache_key = f"{name}_{version}"
        if hasattr(self, '_constants_cache') and cache_key in self._constants_cache:
            return self._constants_cache[cache_key]
        
        # Lazy load
        data_path = _get_data_path()
        json_path = data_path / f"constants/{version}/{name}.json"
        
        if json_path.exists():
            data = json.loads(json_path.read_text())
            result = (data["value"], data.get("unit", ""), data.get("uncertainty", 0.0))
            
            # Cache für Performance
            if not hasattr(self, '_constants_cache'):
                self._constants_cache = {}
            self._constants_cache[cache_key] = result
            return result
        
        self.handle_error(f"Constant '{name}' (version '{version}') not found")
        return None


    def get_info(self):
        """Config Status + Default Version"""
        return {
            'default_version': self.constants.version,      # CODATA2022
            'data_path': _get_data_path(),
            'cache_size': len(getattr(self, '_constants_cache', {})),
            'available_versions': self.list_versions(),
            'loaded_constants': list(getattr(self, '_constants_cache', {}).keys())
        }

    def list_versions(self):
        """Verfügbare CODATA Versionen"""
        data_path = _get_data_path()
        versions = [d.name for d in (data_path / "constants").iterdir() if d.is_dir()]
        return sorted(versions, reverse=True)  # Neueste zuerst

    def status(self):
        """Kurzstatus"""
        print(f"SciLib config: {self.constants.version} | "
            f"{len(getattr(self, '_constants_cache', {}))} cached | "
            f"{_get_data_path()}")
        
            
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