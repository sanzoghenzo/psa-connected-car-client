"""APK parser tests."""
from __future__ import annotations

import datetime
import json
from dataclasses import dataclass

from cryptography import x509
from cryptography.hazmat._oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.x509 import Certificate
from psa_ccc.apk_parser import PFX_PASSWORD
from psa_ccc.apk_parser import ConfigInfo
from psa_ccc.apk_parser import get_config_from_apk


@dataclass
class FakeResources:
    """Fake APK resources."""

    package_name: str = "FakeApp"

    def get_string(self, package_name, key) -> list[str]:
        """Return a string variable."""
        if package_name == self.package_name:
            return ["", "brand_id_url"]


@dataclass
class FakeAPK:
    """Fake APK parser."""

    private_key: RSAPrivateKey
    certificate: Certificate
    package_name: str = "FakeApp"

    def get_package(self) -> str:
        """Returns the package name."""
        return self.package_name

    def get_android_resources(self) -> FakeResources:
        """Returns the apk resources."""
        return FakeResources(self.package_name)

    def get_file(self, path: str) -> str | bytes:
        """Return the contents of the file at the given path."""
        if path == "res/raw/cultures.json":
            return json.dumps({"IT": {"languages": ["it_it"]}})
        if path == "assets/MWPMYMA1.pfx":
            key = self.private_key
            certificate = self.certificate
            return serialization.pkcs12.serialize_key_and_certificates(
                b"test",
                key,
                certificate,
                None,
                serialization.BestAvailableEncryption(PFX_PASSWORD),
            )
        if path == "res/raw-it-rit/parameters.json":
            return json.dumps({"cvsSecret": "TOPSECRET", "cvsClientId": "ClientID"})
        raise FileNotFoundError(path)


def test_get_config_from_apk() -> None:
    """Config info from a fakr APK parser."""
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    cert = _fake_cert(key)
    apk = FakeAPK(key, cert)

    config = get_config_from_apk(apk, "IT", "AP_IT_ESP")
    assert config == ConfigInfo(
        client_id="ClientID",
        client_secret="TOPSECRET",  # noqa S106
        site_code="AP_IT_ESP",
        brand_id="brand_id_url",
        culture="it_it",
        public_certificate=cert.public_bytes(encoding=serialization.Encoding.PEM),
        private_key=key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ),
    )


def _fake_cert(key):
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My Company"),
            x509.NameAttribute(NameOID.COMMON_NAME, "mysite.com"),
        ]
    )
    return (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=10))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName("localhost")]),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )
