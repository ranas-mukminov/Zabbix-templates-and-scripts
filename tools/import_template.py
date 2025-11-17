#!/usr/bin/env python3
"""
Zabbix Template Import Tool via API

This script imports Zabbix template XML files using the Zabbix JSON-RPC API.
It's useful for automating template deployment or bulk importing multiple templates.

Requirements:
    pip install requests

Usage:
    python import_template.py --url http://zabbix.local --user Admin --password zabbix --template /path/to/template.xml

Author: run-as-daemon.ru
License: GPL-2.0
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: 'requests' library not found. Install it with: pip install requests")
    sys.exit(1)


class ZabbixAPI:
    """Simple Zabbix API client for template import."""

    def __init__(self, url, user, password):
        """
        Initialize Zabbix API client.

        Args:
            url: Zabbix web UI URL (e.g., http://zabbix.local or http://192.168.1.100:8080)
            user: Zabbix username
            password: Zabbix password
        """
        self.url = url.rstrip('/') + '/api_jsonrpc.php'
        self.user = user
        self.password = password
        self.auth_token = None
        self.request_id = 0

    def _call(self, method, params=None):
        """
        Make a JSON-RPC API call to Zabbix.

        Args:
            method: API method name (e.g., 'user.login')
            params: Method parameters (dict)

        Returns:
            API response result

        Raises:
            Exception: If API returns an error
        """
        self.request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": self.request_id
        }

        if self.auth_token and method != 'user.login':
            payload["auth"] = self.auth_token

        try:
            response = requests.post(self.url, json=payload, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"HTTP request failed: {e}")

        result = response.json()

        if 'error' in result:
            error = result['error']
            raise Exception(f"Zabbix API error: {error.get('data', error.get('message', 'Unknown error'))}")

        return result.get('result')

    def login(self):
        """
        Authenticate with Zabbix and obtain auth token.

        Raises:
            Exception: If authentication fails
        """
        print(f"Authenticating to Zabbix at {self.url}...")
        try:
            self.auth_token = self._call('user.login', {
                'user': self.user,
                'password': self.password
            })
            print("✓ Authentication successful")
        except Exception as e:
            raise Exception(f"Authentication failed: {e}")

    def import_template(self, xml_content, rules=None):
        """
        Import a template from XML content.

        Args:
            xml_content: Template XML as string
            rules: Import rules (dict). If None, uses defaults.

        Returns:
            Import result

        Raises:
            Exception: If import fails
        """
        if rules is None:
            # Default import rules: create new and update existing
            rules = {
                "discoveryRules": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": False
                },
                "graphs": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": False
                },
                "host_groups": {
                    "createMissing": True
                },
                "hosts": {
                    "createMissing": False,
                    "updateExisting": False
                },
                "httptests": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": False
                },
                "items": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": False
                },
                "maps": {
                    "createMissing": True,
                    "updateExisting": True
                },
                "mediaTypes": {
                    "createMissing": True,
                    "updateExisting": True
                },
                "templateLinkage": {
                    "createMissing": True
                },
                "templates": {
                    "createMissing": True,
                    "updateExisting": True
                },
                "templateScreens": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": False
                },
                "triggers": {
                    "createMissing": True,
                    "updateExisting": True,
                    "deleteMissing": False
                },
                "valueMaps": {
                    "createMissing": True,
                    "updateExisting": True
                }
            }

        print("Importing template...")
        result = self._call('configuration.import', {
            'format': 'xml',
            'source': xml_content,
            'rules': rules
        })
        print("✓ Template imported successfully")
        return result


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Import Zabbix templates via API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Import a single template
  %(prog)s --url http://localhost:8080 --user Admin --password zabbix \\
      --template zbx-templates/zbx-cisco/zbx-cisco-bgp4/zbx-cisco-bgp4.xml

  # Import with custom Zabbix URL
  %(prog)s --url https://zabbix.company.com --user admin --password secret \\
      --template /path/to/template.xml

  # Bulk import (shell script)
  for f in zbx-templates/*/*.xml; do
      %(prog)s --url http://zabbix --user Admin --password zabbix --template "$f"
  done
        """
    )

    parser.add_argument('--url', required=True,
                        help='Zabbix web UI URL (e.g., http://localhost:8080)')
    parser.add_argument('--user', required=True,
                        help='Zabbix username (e.g., Admin)')
    parser.add_argument('--password', required=True,
                        help='Zabbix password')
    parser.add_argument('--template', required=True,
                        help='Path to template XML file')

    args = parser.parse_args()

    # Validate template file
    template_path = Path(args.template)
    if not template_path.exists():
        print(f"Error: Template file not found: {args.template}")
        sys.exit(1)

    if not template_path.is_file():
        print(f"Error: Template path is not a file: {args.template}")
        sys.exit(1)

    # Read template XML
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
    except Exception as e:
        print(f"Error reading template file: {e}")
        sys.exit(1)

    if not xml_content.strip():
        print("Error: Template file is empty")
        sys.exit(1)

    print(f"Template: {template_path.name}")
    print(f"Size: {len(xml_content)} bytes")
    print()

    # Initialize API and import
    try:
        api = ZabbixAPI(args.url, args.user, args.password)
        api.login()
        api.import_template(xml_content)
        print()
        print("=" * 60)
        print("SUCCESS: Template imported successfully!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Go to Zabbix UI → Data collection → Templates")
        print("2. Find the imported template")
        print("3. Link it to a host (Configuration → Hosts → [Host] → Templates)")
        print()
    except Exception as e:
        print()
        print("=" * 60)
        print(f"ERROR: {e}")
        print("=" * 60)
        print()
        print("Troubleshooting:")
        print("- Verify Zabbix URL is correct and accessible")
        print("- Check username and password")
        print("- Ensure template XML is valid")
        print("- Check Zabbix server logs for details")
        sys.exit(1)


if __name__ == '__main__':
    main()
