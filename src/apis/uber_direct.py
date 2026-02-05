"""Uber Direct API client for serviceability checks."""

import os
import requests
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


class UberDirectClient:
    """Client for Uber Direct API."""

    def __init__(self):
        self.client_id = os.getenv('UBER_DIRECT_CLIENT_ID')
        self.client_secret = os.getenv('UBER_DIRECT_CLIENT_SECRET')
        self.customer_id = os.getenv('UBER_DIRECT_CUSTOMER_ID')
        self.base_url = os.getenv('UBER_DIRECT_BASE_URL', 'https://api.uber.com')
        self.auth_url = os.getenv('UBER_DIRECT_AUTH_URL', 'https://auth.uber.com/oauth/v2/token')

        self.access_token = None
        self.token_expires_at = None

    def _get_access_token(self) -> str:
        """Get or refresh OAuth access token."""
        # Check if we have a valid token
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token

        # Request new token
        response = requests.post(
            self.auth_url,
            data={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials',
                'scope': 'eats.deliveries'
            }
        )
        response.raise_for_status()

        data = response.json()
        self.access_token = data['access_token']
        expires_in = data.get('expires_in', 3600)
        self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)

        return self.access_token

    def check_serviceability(self, address: Dict[str, str]) -> Optional[bool]:
        """
        Check if Uber Direct can service an address.

        Args:
            address: Dict with keys: street_address, city, state, zip_code, country

        Returns:
            True if serviceable, False if not, None if error
        """
        try:
            token = self._get_access_token()

            # Format address for Uber API
            pickup_address = f"{address.get('street_address', '')}, {address.get('city', '')}, {address.get('state', '')} {address.get('zip_code', '')}"

            # Use delivery quote endpoint to check serviceability
            # If we can get a quote, the address is serviceable
            url = f"{self.base_url}/v1/customers/{self.customer_id}/delivery_quotes"

            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            payload = {
                'pickup_address': pickup_address,
                'dropoff_address': pickup_address,  # Same address just to test serviceability
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)

            # If we get a 200, the address is serviceable
            if response.status_code == 200:
                return True
            elif response.status_code == 422:  # Unprocessable - likely not serviceable
                return False
            else:
                # Other errors - return None to indicate uncertainty
                print(f"Uber API error {response.status_code}: {response.text}")
                return None

        except Exception as e:
            print(f"Error checking Uber serviceability: {e}")
            return None

    def format_address_from_store(self, store) -> Optional[Dict[str, str]]:
        """Format address from store model for API call."""
        if not store.street_address or not store.city or not store.state:
            return None

        return {
            'street_address': store.street_address,
            'city': store.city,
            'state': store.state,
            'zip_code': store.zip_code or '',
            'country': store.country or 'US'
        }


if __name__ == '__main__':
    # Test
    client = UberDirectClient()
    test_address = {
        'street_address': '123 Main St',
        'city': 'San Francisco',
        'state': 'CA',
        'zip_code': '94102',
        'country': 'US'
    }
    result = client.check_serviceability(test_address)
    print(f"Serviceability: {result}")
