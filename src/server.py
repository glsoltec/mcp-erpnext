#!/usr/bin/env python3
"""MCP Server for ERPNext Integration with Claude"""

import asyncio
import json
import sys
from typing import Any

try:
    from .config import PluginConfig
    from .erpnext_client import ERPNextClient
except ImportError:
    from config import PluginConfig
    from erpnext_client import ERPNextClient


class SimpleERPNextServer:
    """Simple MCP-compatible server for ERPNext"""

    def __init__(self):
        self.config = PluginConfig()
        self.erpnext_client = None
        self.load_config()

    def load_config(self):
        """Load ERPNext configuration"""
        if self.config.has_erpnext_config():
            erpnext_config = self.config.get_erpnext_config()
            self.erpnext_client = ERPNextClient(erpnext_config)

    def configure_erpnext(self, url: str, api_key: str, api_secret: str) -> dict:
        """Configure ERPNext connection"""
        try:
            self.config.set_erpnext_credentials(url, api_key, api_secret)
            self.load_config()
            return {
                "success": True,
                "message": "ERPNext configuration saved successfully"
            }
        except Exception as e:
            return {"error": f"Configuration failed: {str(e)}"}

    def test_connection(self) -> dict:
        """Test ERPNext connection"""
        if not self.erpnext_client:
            return {"error": "ERPNext not configured"}
        return self.erpnext_client.test_connection()

    def get_document(self, doctype: str, name: str) -> dict:
        """Get a document"""
        if not self.erpnext_client:
            return {"error": "ERPNext not configured"}
        return self.erpnext_client.get_document(doctype, name)

    def get_list(self, doctype: str, filters: dict = None, fields: list = None, limit: int = 20) -> dict:
        """Get list of documents"""
        if not self.erpnext_client:
            return {"error": "ERPNext not configured"}
        return self.erpnext_client.get_list(doctype, filters, fields, limit)

    def create_document(self, doctype: str, data: dict) -> dict:
        """Create a document"""
        if not self.erpnext_client:
            return {"error": "ERPNext not configured"}
        return self.erpnext_client.create_document(doctype, data)

    def update_document(self, doctype: str, name: str, data: dict) -> dict:
        """Update a document"""
        if not self.erpnext_client:
            return {"error": "ERPNext not configured"}
        return self.erpnext_client.update_document(doctype, name, data)

    def delete_document(self, doctype: str, name: str) -> dict:
        """Delete a document"""
        if not self.erpnext_client:
            return {"error": "ERPNext not configured"}
        return self.erpnext_client.delete_document(doctype, name)

    def call_method(self, method: str, params: dict = None) -> dict:
        """Call a Frappe method"""
        if not self.erpnext_client:
            return {"error": "ERPNext not configured"}
        return self.erpnext_client.call_method(method, params)

    def get_config(self) -> dict:
        """Get configuration status"""
        return self.config.list_config()

    def process_tool_call(self, tool_name: str, arguments: dict) -> str:
        """Process a tool call and return JSON response"""
        try:
            if tool_name == "configure_erpnext":
                result = self.configure_erpnext(
                    arguments['url'],
                    arguments['api_key'],
                    arguments['api_secret']
                )
            elif tool_name == "test_connection":
                result = self.test_connection()
            elif tool_name == "get_document":
                result = self.get_document(
                    arguments['doctype'],
                    arguments['name']
                )
            elif tool_name == "get_list":
                result = self.get_list(
                    arguments['doctype'],
                    arguments.get('filters'),
                    arguments.get('fields'),
                    arguments.get('limit', 20)
                )
            elif tool_name == "create_document":
                result = self.create_document(
                    arguments['doctype'],
                    arguments['data']
                )
            elif tool_name == "update_document":
                result = self.update_document(
                    arguments['doctype'],
                    arguments['name'],
                    arguments['data']
                )
            elif tool_name == "delete_document":
                result = self.delete_document(
                    arguments['doctype'],
                    arguments['name']
                )
            elif tool_name == "call_method":
                result = self.call_method(
                    arguments['method'],
                    arguments.get('params')
                )
            elif tool_name == "get_config":
                result = self.get_config()
            else:
                result = {"error": f"Unknown tool: {tool_name}"}

            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": str(e)})


def main():
    """Main entry point - simple stdio-based server"""
    server = SimpleERPNextServer()

    print("✅ MCP ERPNext Server Started", file=sys.stderr)
    print("📍 Listening on stdio", file=sys.stderr)
    print("🔌 Ready to receive commands from Claude", file=sys.stderr)

    # Simple line-based protocol for testing
    try:
        while True:
            line = input()
            if not line:
                continue

            try:
                data = json.loads(line)
                tool_name = data.get("tool")
                arguments = data.get("args", {})
                result = server.process_tool_call(tool_name, arguments)
                print(result)
            except json.JSONDecodeError:
                print(json.dumps({"error": "Invalid JSON"}))
            except Exception as e:
                print(json.dumps({"error": str(e)}))
    except KeyboardInterrupt:
        print("\n✅ Server stopped", file=sys.stderr)
        sys.exit(0)
    except EOFError:
        print("✅ Server stopped (EOF)", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
