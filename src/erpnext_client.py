import requests
import json
from typing import Any, Dict, List, Optional
from requests.auth import HTTPBasicAuth
from .config import ERPNextConfig

class ERPNextClient:
    def __init__(self, config: ERPNextConfig):
        self.url = config.url.rstrip('/')
        self.api_key = config.api_key
        self.api_secret = config.api_secret
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(self.api_key, self.api_secret)
        self.headers = {'Content-Type': 'application/json'}

    def test_connection(self) -> Dict[str, Any]:
        """Test connection to ERPNext server"""
        try:
            response = self.session.get(
                f"{self.url}/api/method/frappe.client.get_list",
                params={'doctype': 'User', 'limit_page_length': 1},
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return {'success': True, 'message': 'Connection successful'}
            else:
                return {'success': False, 'message': f'HTTP {response.status_code}'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def get_document(self, doctype: str, name: str) -> Dict[str, Any]:
        """Get a single document"""
        try:
            response = self.session.get(
                f"{self.url}/api/resource/{doctype}/{name}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}

    def get_list(self, doctype: str, filters: Optional[Dict] = None,
                 fields: Optional[List[str]] = None, limit: int = 20) -> Dict[str, Any]:
        """Get list of documents"""
        try:
            params = {
                'limit_page_length': limit,
            }
            if fields:
                params['fields'] = json.dumps(fields)
            if filters:
                params['filters'] = json.dumps(filters)

            response = self.session.get(
                f"{self.url}/api/resource/{doctype}",
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}

    def create_document(self, doctype: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new document"""
        try:
            response = self.session.post(
                f"{self.url}/api/resource/{doctype}",
                json=data,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}

    def update_document(self, doctype: str, name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing document"""
        try:
            response = self.session.put(
                f"{self.url}/api/resource/{doctype}/{name}",
                json=data,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}

    def delete_document(self, doctype: str, name: str) -> Dict[str, Any]:
        """Delete a document"""
        try:
            response = self.session.delete(
                f"{self.url}/api/resource/{doctype}/{name}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return {'success': True, 'message': f'{doctype} {name} deleted'}
        except Exception as e:
            return {'error': str(e)}

    def call_method(self, method: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Call a Frappe/ERPNext server method"""
        try:
            response = self.session.post(
                f"{self.url}/api/method/{method}",
                json=params or {},
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}

    def get_report(self, report_name: str, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """Get a report"""
        try:
            params = filters or {}
            response = self.session.get(
                f"{self.url}/api/method/frappe.desk.reportview.get",
                params={
                    'report_name': report_name,
                    'filters': json.dumps(params),
                    'order_by': '`tabUser`.`modified` desc'
                },
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}

    def get_meta(self, doctype: str) -> Dict[str, Any]:
        """Get metadata for a doctype"""
        try:
            response = self.session.get(
                f"{self.url}/api/method/frappe.client.get_meta",
                params={'doctype': doctype},
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}
