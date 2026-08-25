import base64
import json
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from techverify.protocol import canonical_receipt, signing_payload, verify_signature


def did_from_public_key(public_key: bytes) -> str:
    # Minimal base58btc encoder for the test vector.
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    data = b"\xed\x01" + public_key
    n = int.from_bytes(data, "big")
    out = ""
    while n:
        n, r = divmod(n, 58)
        out = alphabet[r] + out
    return "did:key:z" + out


def test_round_trip_and_tamper_detection():
    private = Ed25519PrivateKey.generate()
    did = did_from_public_key(private.public_key().public_bytes_raw())
    room, nonce, text = "lobby", 42, "hello\u200bworld"
    signature = base64.urlsafe_b64encode(private.sign(signing_payload(room, nonce, text))).rstrip(b"=").decode()

    assert verify_signature(did, signature, room, nonce, text)
    assert not verify_signature(did, signature, room, nonce, "hello world!")

    receipt = canonical_receipt(did, room, nonce, text, signature)
    assert receipt["text"] == "hello world"
    assert receipt["type"] == "technocore-receipt"


def test_live_technocore_vector_verifies():
    vector = json.loads((Path(__file__).parents[1] / "vectors" / "live.json").read_text())

    assert vector["source"] == "technocore.chat"
    assert vector["kind"] == "live-signed-message"
    assert verify_signature(
        vector["did"],
        vector["signature"],
        vector["room"],
        int(vector["nonce"]),
        vector["text"],
    )
