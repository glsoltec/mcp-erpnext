#!/usr/bin/env python3
"""MCP Server for ERPNext Integration with Claude"""

import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from config import PluginConfig
from erpnext_client import ERPNextClient

class ConfigRequest(BaseModel):
    url: str
    api_key: str
    api_secret: str

class Server:
    def __init__(self):
        self.server = Server("mcp-erpnext")
        self.config = PluginConfig()
        self.erpnext_client = None
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup MCP request handlers"""
        @self.server.call_tool()
        async def handle_tool_call(name: str, arguments: dict) -> str:
            return await self._execute_tool(name, arguments)

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return self._get_available_tools()

    async def _execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Execute a tool request"""
        try:
            if tool_name == "configure_erpnext":
                return self._configure_erpnext(arguments)
            elif tool_name == "test_connection":
                return self._test_connection()
            elif tool_name == "get_document":
                return self._get_document(arguments)
            elif tool_name == "get_list":
                return self._get_list(arguments)
            elif tool_name == "create_document":
                return self._create_document(arguments)
            elif tool_name == "update_document":
                return self._update_document(arguments)
            elif tool_name == "delete_document":
                return self._delete_document(arguments)
            elif tool_name == "call_method":
                return self._call_method(arguments)
            elif tool_name == "get_config":
                return self._get_config()
            else:
                return json.dumps({"error": f"Unknown tool: {tool_name}"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def _configure_erpnext(self, args: dict) -> str:
        """Configure ERPNext connection"""
        try:
            self.config.set_erpnext_credentials(
                url=args['url'],
                api_key=args['api_key'],
                api_secret=args['api_secret']
            )
            config = self.config.get_erpnext_config()
            self.erpnext_client = ERPNextClient(config)
            return json.dumps({
                "success": True,
                "message": "ERPNext configuration saved successfully"
            })
        except Exception as e:
            return json.dumps({"error": f"Configuration failed: {str(e)}"})

    def _test_connection(self) -> str:
        """Test ERPNext connection"""
        if not self.config.has_erpnext_config():
            return json.dumps({
                "error": "ERPNext not configured. Use configure_erpnext first."
            })

        if not self.erpnext_client:
            config = self.config.get_erpnext_config()
            self.erpnext_client = ERPNextClient(config)

        result = self.erpnext_client.test_connection()
        return json.dumps(result)

    def _get_document(self, args: dict) -> str:
        """Get a document from ERPNext"""
        if not self.erpnext_client:
            return json.dumps({"error": "ERPNext not configured"})

        result = self.erpnext_client.get_document(
            doctype=args['doctype'],
            name=args['name']
        )
        return json.dumps(result)

    def _get_list(self, args: dict) -> str:
        """Get a list of documents from ERPNext"""
        if not self.erpnext_client:
            return json.dumps({"error": "ERPNext not configured"})

        result = self.erpnext_client.get_list(
            doctype=args['doctype'],
            filters=args.get('filters'),
            fields=args.get('fields'),
            limit=args.get('limit', 20)
        )
        return json.dumps(result)

    def _create_document(self, args: dict) -> str:
        """Create a document in ERPNext"""
        if not self.erpnext_client:
            return json.dumps({"error": "ERPNext not configured"})

        result = self.erpnext_client.create_document(
            doctype=args['doctype'],
            data=args['data']
        )
        return json.dumps(result)

    def _update_document(self, args: dict) -> str:
        """Update a document in ERPNext"""
        if not self.erpnext_client:
            return json.dumps({"error": "ERPNext not configured"})

        result = self.erpnext_client.update_document(
            doctype=args['doctype'],
            name=args['name'],
            data=args['data']
        )
        return json.dumps(result)

    def _delete_document(self, args: dict) -> str:
        """Delete a document from ERPNext"""
        if not self.erpnext_client:
            return json.dumps({"error": "ERPNext not configured"})

        result = self.erpnext_client.delete_document(
            doctype=args['doctype'],
            name=args['name']
        )
        return json.dumps(result)

    def _call_method(self, args: dict) -> str:
        """Call a Frappe/ERPNext method"""
        if not self.erpnext_client:
            return json.dumps({"error": "ERPNext not configured"})

        result = self.erpnext_client.call_method(
            method=args['method'],
            params=args.get('params')
        )
        return json.dumps(result)

    def _get_config(self) -> str:
        """Get current configuration"""
        config = self.config.list_config()
        return json.dumps(config)

    def _get_available_tools(self) -> List[Tool]:
        """Return available tools for Claude"""
        return [
            Tool(
                name="configure_erpnext",
                description="Configure ERPNext connection with URL, API Key, and API Secret",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "ERPNext instance URL (e.g., https://your-instance.erpnext.com)"},
                        "api_key": {"type": "string", "description": "ERPNext API Key"},
                        "api_secret": {"type": "string", "description": "ERPNext API Secret"}
                    },
                    "required": ["url", "api_key", "api_secret"]
                }
            ),
            Tool(
                name="test_connection",
                description="Test connection to ERPNext server",
                inputSchema={"type": "object", "properties": {}}
            ),
            Tool(
                name="get_document",
                description="Get a specific document from ERPNext",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doctype": {"type": "string", "description": "Document type (e.g., 'Customer', 'Invoice')"},
                        "name": {"type": "string", "description": "Document name/ID"}
                    },
                    "required": ["doctype", "name"]
                }
            ),
            Tool(
                name="get_list",
                description="Get a list of documents from ERPNext",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doctype": {"type": "string", "description": "Document type"},
                        "filters": {"type": "object", "description": "Filter conditions"},
                        "fields": {"type": "array", "items": {"type": "string"}, "description": "Fields to return"},
                        "limit": {"type": "integer", "description": "Limit results", "default": 20}
                    },
                    "required": ["doctype"]
                }
            ),
            Tool(
                name="create_document",
                description="Create a new document in ERPNext",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doctype": {"type": "string", "description": "Document type"},
                        "data": {"type": "object", "description": "Document data/fields"}
                    },
                    "required": ["doctype", "data"]
                }
            ),
            Tool(
                name="update_document",
                description="Update an existing document in ERPNext",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doctype": {"type": "string", "description": "Document type"},
                        "name": {"type": "string", "description": "Document name/ID"},
                        "data": {"type": "object", "description": "Fields to update"}
                    },
                    "required": ["doctype", "name", "data"]
                }
            ),
            Tool(
                name="delete_document",
                description="Delete a document from ERPNext",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doctype": {"type": "string", "description": "Document type"},
                        "name": {"type": "string", "description": "Document name/ID"}
                    },
                    "required": ["doctype", "name"]
                }
            ),
            Tool(
                name="call_method",
                description="Call a Frappe/ERPNext server method",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "method": {"type": "string", "description": "Method name (e.g., 'frappe.client.get_list')"},
                        "params": {"type": "object", "description": "Method parameters"}
                    },
                    "required": ["method"]
                }
            ),
            Tool(
                name="get_config",
                description="Get current configuration status",
                inputSchema={"type": "object", "properties": {}}
            )
        ]

    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream)


async def main():
    """Main entry point"""
    server = Server()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
