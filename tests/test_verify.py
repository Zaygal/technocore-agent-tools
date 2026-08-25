import base64

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from technocore_agent_tools.verify import verify_signature


def test_valid_signature_round_trip():
    private = Ed25519PrivateKey.generate()
    public = private.public_key().public_bytes_raw()
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    value = int.from_bytes(b"\xed\x01" + public, "big")
    encoded = ""
    while value:
        value, remainder = divmod(value, 58)
        encoded = alphabet[remainder] + encoded
    did = "did:key:z" + encoded
    payload = "room|1|hello"
    signature = base64.urlsafe_b64encode(private.sign(payload.encode())).rstrip(b"=").decode()
    assert verify_signature(did, signature, payload)
    assert not verify_signature(did, signature, "room|1|tampered")
