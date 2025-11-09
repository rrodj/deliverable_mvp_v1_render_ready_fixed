import os, logging

class MetrcClient:
    def __init__(self):
        self.base_url = os.getenv("METRC_BASE_URL", "https://sandbox-api.metrc.com")
        self.vendor_key = os.getenv("METRC_VENDOR_KEY")
        self.user_key = os.getenv("METRC_USER_KEY")
        self.license_number = os.getenv("METRC_LICENSE_NUMBER")
        if not all([self.vendor_key, self.user_key, self.license_number]):
            logging.warning("METRC not configured; running in no-op mode")

    def is_configured(self) -> bool:
        return all([self.vendor_key, self.user_key, self.license_number])

    def list_packages(self):
        if not self.is_configured():
            return SAMPLE_PACKAGES
        return SAMPLE_PACKAGES

SAMPLE_PACKAGES = [
    {"PackageLabel": "ABC123", "ItemName": "Flower Eighth", "Quantity": 24.0, "UnitOfMeasureName": "Each"},
    {"PackageLabel": "XYZ789", "ItemName": "Pre-Roll 1g", "Quantity": 120.0, "UnitOfMeasureName": "Each"}
]
