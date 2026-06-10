#!/usr/bin/env python3
"""Example usage of the ERPNext MCP Plugin"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import PluginConfig
from erpnext_client import ERPNextClient


def main():
    """Example: Configure and use ERPNext client"""

    # Initialize configuration
    config = PluginConfig()

    # Example 1: Check if configured
    print("=== ERPNext Plugin Example ===\n")

    if not config.has_erpnext_config():
        print("ERPNext not configured. Please run:")
        print("  python src/cli.py configure --interactive\n")
        return

    # Get configuration
    erpnext_config = config.get_erpnext_config()
    print(f"✓ Connected to: {erpnext_config.url}\n")

    # Create client
    client = ERPNextClient(erpnext_config)

    # Example 2: Test connection
    print("--- Testing Connection ---")
    result = client.test_connection()
    print(f"Result: {result}\n")

    if not result.get('success'):
        print("Connection failed. Please check your credentials.")
        return

    # Example 3: Get list of customers
    print("--- Getting Customer List ---")
    result = client.get_list('Customer', limit=5)
    if 'data' in result:
        for customer in result['data']:
            print(f"  - {customer.get('name', 'N/A')}: {customer.get('customer_name', 'N/A')}")
    else:
        print(f"  {result}\n")

    # Example 4: Get list with filters
    print("\n--- Getting Invoices (Draft Status) ---")
    result = client.get_list(
        'Invoice',
        filters={'docstatus': 0},  # 0 = Draft
        fields=['name', 'customer', 'grand_total'],
        limit=5
    )
    if 'data' in result:
        print(f"Found {len(result['data'])} draft invoices:")
        for invoice in result['data']:
            print(f"  - {invoice.get('name')}: {invoice.get('customer')} - R$ {invoice.get('grand_total')}")
    else:
        print(f"  {result}\n")

    # Example 5: Get document meta
    print("\n--- Getting Document Metadata (Customer) ---")
    result = client.get_meta('Customer')
    if 'message' in result:
        meta = result['message']
        print(f"  Doctype: {meta.get('name')}")
        print(f"  Module: {meta.get('module')}")
        print(f"  Fields: {len(meta.get('fields', []))} fields")
    else:
        print(f"  {result}\n")

    # Example 6: Call a server method
    print("\n--- Calling Server Method ---")
    result = client.call_method(
        'frappe.client.get_count',
        params={'doctype': 'Customer'}
    )
    print(f"Total customers: {result.get('message', 'N/A')}\n")

    # Example 7: Create a document (commented out to avoid creating dummy data)
    # print("--- Creating a Document ---")
    # result = client.create_document(
    #     'Customer',
    #     {
    #         'customer_name': 'Test Customer',
    #         'customer_type': 'Individual',
    #         'country': 'Brazil'
    #     }
    # )
    # print(f"Result: {result}\n")

    # Example 8: Update a document (commented out)
    # print("--- Updating a Document ---")
    # result = client.update_document(
    #     'Customer',
    #     'CUST-001',
    #     {'customer_name': 'Updated Name'}
    # )
    # print(f"Result: {result}\n")

    print("=== Example Complete ===")


if __name__ == '__main__':
    main()
