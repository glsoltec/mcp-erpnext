import os
import json
from pathlib import Path
from pydantic import BaseModel
from typing import Optional

class ERPNextConfig(BaseModel):
    url: str
    api_key: str
    api_secret: str

    class Config:
        extra = "allow"

class PluginConfig:
    CONFIG_DIR = Path.home() / ".mcp-erpnext"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    def __init__(self):
        self.CONFIG_DIR.mkdir(exist_ok=True)
        self._config = self._load_config()

    def _load_config(self) -> dict:
        if self.CONFIG_FILE.exists():
            with open(self.CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {}

    def _save_config(self):
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self._config, f, indent=2)

    def set_erpnext_credentials(self, url: str, api_key: str, api_secret: str):
        """Set ERPNext connection credentials"""
        self._config['erpnext'] = {
            'url': url,
            'api_key': api_key,
            'api_secret': api_secret
        }
        self._save_config()

    def get_erpnext_config(self) -> Optional[ERPNextConfig]:
        """Get ERPNext configuration"""
        if 'erpnext' in self._config:
            return ERPNextConfig(**self._config['erpnext'])
        return None

    def set_claude_key(self, api_key: str):
        """Set Claude API key"""
        self._config['claude'] = {'api_key': api_key}
        self._save_config()

    def get_claude_key(self) -> Optional[str]:
        """Get Claude API key"""
        if 'claude' in self._config:
            return self._config['claude'].get('api_key')
        return None

    def has_erpnext_config(self) -> bool:
        """Check if ERPNext configuration exists"""
        return 'erpnext' in self._config

    def list_config(self) -> dict:
        """List all configuration (without sensitive data)"""
        safe_config = {}
        if 'erpnext' in self._config:
            safe_config['erpnext'] = {
                'url': self._config['erpnext']['url'],
                'configured': True
            }
        if 'claude' in self._config:
            safe_config['claude'] = {'configured': True}
        return safe_config
