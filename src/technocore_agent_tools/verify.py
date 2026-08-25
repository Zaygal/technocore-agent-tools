"""Offline verification for Ed25519 ``did:key`` identifiers."""

import base64
import binascii

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

_PREFIX = b"\xed\x01"
_DID_PREFIX = "did:key:z"


def _decode_base58(value: str) -> bytes:
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    n = 0
    for char in value:
        try:
            n = n * 58 + alphabet.index(char)
        except ValueError as exc:
            raise ValueError("invalid base58btc DID") from exc
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    pad = len(value) - len(value.lstrip("1"))
    return b"\0" * pad + raw


def public_key_from_did(did: str) -> Ed25519PublicKey:
    """Extract the Ed25519 public key from a ``did:key:z...`` DID."""
    if not did.startswith(_DID_PREFIX):
        raise ValueError("expected an Ed25519 did:key")
    decoded = _decode_base58(did[len(_DID_PREFIX) :])
    if not decoded.startswith(_PREFIX) or len(decoded) != 34:
        raise ValueError("DID does not contain an Ed25519 multicodec key")
    return Ed25519PublicKey.from_public_bytes(decoded[2:])


def verify_signature(did: str, signature_b64url: str, payload: bytes | str) -> bool:
    """Return True only when the DID's public key verifies the signature."""
    if isinstance(payload, str):
        payload = payload.encode("utf-8")
    try:
        signature = base64.urlsafe_b64decode(signature_b64url + "=" * (-len(signature_b64url) % 4))
        public_key_from_did(did).verify(signature, payload)
    except (ValueError, binascii.Error, InvalidSignature):
        return False
    return True
