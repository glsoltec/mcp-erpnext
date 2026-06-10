#!/usr/bin/env python3
"""Tests for configuration module"""

import unittest
import sys
import os
from pathlib import Path
import tempfile
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import PluginConfig, ERPNextConfig


class TestPluginConfig(unittest.TestCase):
    """Test configuration management"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_config_dir = PluginConfig.CONFIG_DIR
        PluginConfig.CONFIG_DIR = Path(self.temp_dir.name)
        PluginConfig.CONFIG_FILE = Path(self.temp_dir.name) / "config.json"

    def tearDown(self):
        """Clean up after tests"""
        PluginConfig.CONFIG_DIR = self.original_config_dir
        PluginConfig.CONFIG_FILE = self.original_config_dir / "config.json"
        self.temp_dir.cleanup()

    def test_set_and_get_erpnext_credentials(self):
        """Test setting and getting ERPNext credentials"""
        config = PluginConfig()

        config.set_erpnext_credentials(
            url="https://test.erpnext.com",
            api_key="test_key",
            api_secret="test_secret"
        )

        result = config.get_erpnext_config()
        self.assertIsNotNone(result)
        self.assertEqual(result.url, "https://test.erpnext.com")
        self.assertEqual(result.api_key, "test_key")
        self.assertEqual(result.api_secret, "test_secret")

    def test_has_erpnext_config(self):
        """Test checking if ERPNext is configured"""
        config = PluginConfig()
        self.assertFalse(config.has_erpnext_config())

        config.set_erpnext_credentials(
            url="https://test.erpnext.com",
            api_key="test_key",
            api_secret="test_secret"
        )
        self.assertTrue(config.has_erpnext_config())

    def test_list_config_without_sensitive_data(self):
        """Test that list_config doesn't expose sensitive data"""
        config = PluginConfig()
        config.set_erpnext_credentials(
            url="https://test.erpnext.com",
            api_key="secret_key",
            api_secret="secret_secret"
        )

        result = config.list_config()
        self.assertIn('erpnext', result)
        self.assertIn('url', result['erpnext'])
        self.assertNotIn('api_key', result['erpnext'])
        self.assertNotIn('api_secret', result['erpnext'])

    def test_set_and_get_claude_key(self):
        """Test setting and getting Claude API key"""
        config = PluginConfig()

        config.set_claude_key("claude_test_key")
        result = config.get_claude_key()

        self.assertEqual(result, "claude_test_key")

    def test_config_persistence(self):
        """Test that configuration persists to file"""
        config1 = PluginConfig()
        config1.set_erpnext_credentials(
            url="https://test.erpnext.com",
            api_key="test_key",
            api_secret="test_secret"
        )

        config2 = PluginConfig()
        result = config2.get_erpnext_config()

        self.assertIsNotNone(result)
        self.assertEqual(result.url, "https://test.erpnext.com")


class TestERPNextConfig(unittest.TestCase):
    """Test ERPNextConfig model"""

    def test_erpnext_config_creation(self):
        """Test creating ERPNextConfig instance"""
        config = ERPNextConfig(
            url="https://test.erpnext.com",
            api_key="test_key",
            api_secret="test_secret"
        )

        self.assertEqual(config.url, "https://test.erpnext.com")
        self.assertEqual(config.api_key, "test_key")
        self.assertEqual(config.api_secret, "test_secret")

    def test_erpnext_config_validation(self):
        """Test ERPNextConfig validation"""
        with self.assertRaises(Exception):
            ERPNextConfig(
                url="https://test.erpnext.com",
                api_key="test_key"
                # Missing api_secret
            )


if __name__ == '__main__':
    unittest.main()
