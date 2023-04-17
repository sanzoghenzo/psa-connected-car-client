"""Brand related configuration."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BrandConfig:
    """Brand configuration."""

    name: str
    brand_code: str
    mqtt_brand_code: str
    app_name: str
    app_code: str
    tld: str
    realm: str

    @property
    def access_token_url(self) -> str:
        """URL to retrieve the token."""
        return f"https://idpcvs.{self.tld}/am/oauth2/access_token"

    def site_code(self, country_code: str) -> str:
        """Site code."""
        return f"{self.brand_code}_{country_code}_ESP"

    @property
    def user_url(self) -> str:
        """URL of the user info."""
        return f"https://mw-{self.brand_code.lower()}-m2c.mym.awsmpsa.com/api/v1/user"

    def customer_id(self, user_id: str) -> str:
        """Customer ID for MQTT communication."""
        return f"{self.mqtt_brand_code}-{user_id}"

    @property
    def apk_name(self) -> str:
        """Name of the APK file."""
        return f"{self.app_code.split('.')[-1]}.apk"


BRAND_CONFIG_MAP = {
    "Peugeot": BrandConfig(
        name="Peugeot",
        tld="peugeot.com",
        realm="clientsB2CPeugeot",
        app_code="com.psa.mym.mypeugeot",
        brand_code="AP",
        mqtt_brand_code="AP",
        app_name="MyPeugeot",
    ),
    "Citroen": BrandConfig(
        name="Citroen",
        tld="citroen.com",
        realm="clientsB2CCitroen",
        app_code="com.psa.mym.mycitroen",
        brand_code="AC",
        mqtt_brand_code="AC",
        app_name="MyCitroen",
    ),
    "DS": BrandConfig(
        name="DS",
        tld="driveds.com",
        realm="clientsB2CDS",
        app_code="com.psa.mym.myds",
        brand_code="DS",
        mqtt_brand_code="AC",
        app_name="MyDS",
    ),
    "Opel": BrandConfig(
        name="Opel",
        tld="opel.com",
        realm="clientsB2COpel",
        app_code="com.psa.mym.myopel",
        brand_code="OP",
        mqtt_brand_code="OV",
        app_name="MyOpel",
    ),
    "Vauxhall": BrandConfig(
        name="Vauxhall",
        tld="vauxhall.co.uk",
        realm="clientsB2CVauxhall",
        app_code="com.psa.mym.myvauxhall",
        brand_code="VX",
        mqtt_brand_code="OV",
        app_name="MyVauxhall",
    ),
}
