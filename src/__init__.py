"""MCP ERPNext Plugin"""

from .config import PluginConfig, ERPNextConfig
from .erpnext_client import ERPNextClient

__version__ = "1.0.0"
__all__ = ["PluginConfig", "ERPNextConfig", "ERPNextClient"]
