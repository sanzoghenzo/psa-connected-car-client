"""Brand Config tests."""
from __future__ import annotations

from psa_ccc.brand_config import BRAND_CONFIG_MAP

bc = BRAND_CONFIG_MAP["Peugeot"]


def test_peugeot_token_url() -> None:
    assert (
        bc.access_token_url
        == "https://idpcvs.peugeot.com/am/oauth2/access_token"  # noqa S105
    )


def test_peugeot_site_code() -> None:
    assert bc.site_code("IT") == "AP_IT_ESP"


def test_peugeot_user_url() -> None:
    assert bc.user_url == "https://mw-ap-m2c.mym.awsmpsa.com/api/v1/user"


def test_peugeot_customer_id() -> None:
    assert bc.customer_id("userid") == "AP-userid"


def test_peugeot_apk_name() -> None:
    assert bc.apk_name == "mypeugeot.apk"
