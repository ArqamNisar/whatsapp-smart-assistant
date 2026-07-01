import os
import requests
from dotenv import load_dotenv

class WhatsAppBusinessClient:
    def __init__(self, env_path=".env"):
        self.env_path = env_path
        self.access_token = None
        self.phone_number_id = None
        self.business_account_id = None
        self.load_credentials()

    def load_credentials(self):
        """Loads credentials from the .env file if it exists."""
        if os.path.exists(self.env_path):
            load_dotenv(self.env_path, override=True)
            self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
            self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
            self.business_account_id = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID")
            return True
        return False

    def save_credentials(self, access_token, phone_number_id, business_account_id):
        """Saves credentials to the .env file."""
        existing = {}
        if os.path.exists(self.env_path):
            with open(self.env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line and not line.startswith("#"):
                        parts = line.split("=", 1)
                        if len(parts) == 2:
                            existing[parts[0].strip()] = parts[1].strip()

        # Update or set variables
        existing["WHATSAPP_ACCESS_TOKEN"] = access_token
        existing["WHATSAPP_PHONE_NUMBER_ID"] = phone_number_id
        existing["WHATSAPP_BUSINESS_ACCOUNT_ID"] = business_account_id

        # Write back to .env
        with open(self.env_path, "w", encoding="utf-8") as f:
            for k, v in existing.items():
                f.write(f"{k}={v}\n")

        # Refresh local variables
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.business_account_id = business_account_id

    def clear_credentials(self):
        """Removes the credentials from the class state and .env file."""
        if os.path.exists(self.env_path):
            existing = {}
            with open(self.env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line and not line.startswith("#"):
                        parts = line.split("=", 1)
                        if len(parts) == 2:
                            existing[parts[0].strip()] = parts[1].strip()
            
            # Remove keys if they exist
            existing.pop("WHATSAPP_ACCESS_TOKEN", None)
            existing.pop("WHATSAPP_PHONE_NUMBER_ID", None)
            existing.pop("WHATSAPP_BUSINESS_ACCOUNT_ID", None)

            with open(self.env_path, "w", encoding="utf-8") as f:
                for k, v in existing.items():
                    f.write(f"{k}={v}\n")

        self.access_token = None
        self.phone_number_id = None
        self.business_account_id = None

    def verify_credentials(self, access_token, phone_number_id, business_account_id):
        """
        Validates WhatsApp credentials by querying the Meta Graph API.
        Returns (success: bool, info_or_error: str/dict)
        """
        if not access_token or not phone_number_id or not business_account_id:
            return False, "All fields (Access Token, Phone Number ID, Business ID) are required."

        # We query the phone number node which is quick and verifies the token and ID
        url = f"https://graph.facebook.com/v20.0/{phone_number_id}"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Verify that the response belongs to the expected business account if needed
                return True, data
            else:
                try:
                    error_info = response.json().get("error", {})
                    err_msg = error_info.get("message", "Unknown Meta Graph API error.")
                    return False, f"API Error: {err_msg}"
                except Exception:
                    return False, f"HTTP Error {response.status_code}: {response.text}"
        except requests.exceptions.RequestException as e:
            return False, f"Network Connection Failed: {str(e)}"
