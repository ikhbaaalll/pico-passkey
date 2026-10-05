#!/usr/bin/env python3
"""Smoke check for a pico-fido device.

Default: list the FIDO HID device and print its CTAP info.
--register: make a discoverable credential for example.com, then assert with it.
Exit non-zero when no device answers.
"""

import sys
from fido2.client import Fido2Client, UserInteraction
from fido2.ctap2 import Ctap2
from fido2.hid import CtapHidDevice

RP_ID = "example.com"
ORIGIN = f"https://{RP_ID}"


class Touch(UserInteraction):
    def prompt_up(self):
        print("touch the key now (BOOT button)...")

    def request_pin(self, permissions, rd_id):
        return input("key PIN: ")

    def request_uv(self, permissions, rd_id):
        print("user verification required")
        return True


def main() -> int:
    devices = list(CtapHidDevice.list_devices())
    if not devices:
        print("FAIL: no FIDO HID device. Cable charge-only? Wrong firmware? BOOT not held?")
        return 1

    dev = devices[0]
    info = Ctap2(dev).info
    versions = " ".join(str(v) for v in (info.versions or []))
    print(f"device: {dev.descriptor.product_name}")
    print(f"CTAP versions: {versions}")
    options = info.options or {}
    print(f"discoverable credentials (rk): {'yes' if options.get('rk') else 'no'}")
    print(f"user verification (uv): {'yes' if options.get('uv') else 'no'}")
    if info.remaining_disc_creds is not None:
        print(f"free passkey slots: {info.remaining_disc_creds}")

    if "--register" not in sys.argv:
        return 0

    client = Fido2Client(dev, ORIGIN, user_interaction=Touch())
    creation = client.make_credential(
        {
            "rp": {"id": RP_ID, "name": "pico-passkey smoke"},
            "user": {"id": b"smoke-user", "name": "smoke"},
            "challenge": b"smoke-challenge-32-bytes-long!!!",
            "pubKeyCredParams": [{"type": "public-key", "alg": -7}],
            "authenticatorSelection": {"residentKey": "required", "userVerification": "preferred"},
        }
    )
    assert creation.attestation_object is not None, "no attestation object"
    print(f"registered: credential {creation.attestation_object.auth_data.credential_data.credential_id.hex()[:16]}...")

    assertion = client.get_assertion(
        {
            "rpId": RP_ID,
            "challenge": b"smoke-assert-challenge-32-bytes!!",
            "allowCredentials": [],
        }
    )
    result = assertion.get_response(0)
    assert result.signature, "empty signature"
    print(f"asserted: {len(result.signature)} byte signature")
    print("PASS: make_credential + get_assertion both answered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
