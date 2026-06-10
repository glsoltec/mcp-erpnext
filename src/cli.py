#!/usr/bin/env python3
"""CLI for MCP ERPNext Plugin Configuration"""

import argparse
import json
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import PluginConfig
from erpnext_client import ERPNextClient


def configure_command(args):
    """Configure ERPNext connection"""
    config = PluginConfig()

    if args.interactive:
        print("\n=== ERPNext Configuration Setup ===\n")
        url = input("Enter ERPNext URL (e.g., https://your-instance.erpnext.com): ").strip()
        api_key = input("Enter API Key: ").strip()
        api_secret = input("Enter API Secret: ").strip()
    else:
        url = args.url
        api_key = args.api_key
        api_secret = args.api_secret

    try:
        config.set_erpnext_credentials(url, api_key, api_secret)
        print("\n✓ Configuration saved successfully!")
        print(f"  URL: {url}")
        print(f"  Config file: {config.CONFIG_FILE}\n")
    except Exception as e:
        print(f"✗ Configuration failed: {e}", file=sys.stderr)
        sys.exit(1)


def test_command(args):
    """Test ERPNext connection"""
    config = PluginConfig()

    if not config.has_erpnext_config():
        print("✗ ERPNext not configured. Run: mcp-erpnext configure", file=sys.stderr)
        sys.exit(1)

    try:
        erpnext_config = config.get_erpnext_config()
        client = ERPNextClient(erpnext_config)
        result = client.test_connection()

        if result.get('success'):
            print("\n✓ Connection successful!")
            print(f"  Message: {result.get('message')}\n")
        else:
            print(f"\n✗ Connection failed: {result.get('message')}\n")
            sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def status_command(args):
    """Show configuration status"""
    config = PluginConfig()
    status = config.list_config()

    print("\n=== Configuration Status ===\n")
    if status:
        print(json.dumps(status, indent=2))
    else:
        print("No configuration found.")
    print()


def show_command(args):
    """Show full configuration file location"""
    config = PluginConfig()
    print(f"\nConfiguration file: {config.CONFIG_FILE}")
    print(f"Config directory: {config.CONFIG_DIR}\n")


def main():
    parser = argparse.ArgumentParser(
        description="MCP ERPNext Plugin Configuration Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive configuration
  mcp-erpnext configure --interactive

  # Configure with arguments
  mcp-erpnext configure --url https://your-instance.erpnext.com --api-key KEY --api-secret SECRET

  # Test connection
  mcp-erpnext test

  # Show configuration status
  mcp-erpnext status

  # Show configuration file location
  mcp-erpnext show
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Configure command
    configure_parser = subparsers.add_parser('configure', help='Configure ERPNext connection')
    configure_parser.add_argument('--interactive', '-i', action='store_true',
                                  help='Interactive configuration mode')
    configure_parser.add_argument('--url', help='ERPNext instance URL')
    configure_parser.add_argument('--api-key', help='API Key')
    configure_parser.add_argument('--api-secret', help='API Secret')
    configure_parser.set_defaults(func=configure_command)

    # Test command
    test_parser = subparsers.add_parser('test', help='Test ERPNext connection')
    test_parser.set_defaults(func=test_command)

    # Status command
    status_parser = subparsers.add_parser('status', help='Show configuration status')
    status_parser.set_defaults(func=status_command)

    # Show command
    show_parser = subparsers.add_parser('show', help='Show configuration file location')
    show_parser.set_defaults(func=show_command)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == '__main__':
    main()
