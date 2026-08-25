"""Technocore-compatible signing and verification primitives."""
from __future__ import annotations

import base64
import json
import re
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

DID_RE = re.compile(r"^did:key:z([A-Za-z0-9_-]+)$")


def normalize_text(text: str) -> str:
    """Match Technocore's single-line normalization: invisible characters -> spaces."""
    return "".join(" " if (ch.isspace() or ch in "\u200b\u200c\u200d\ufeff\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069") else ch for ch in text).replace("\n", " ")


def _b64url_decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def public_key_from_did(did: str) -> Ed25519PublicKey:
    """Decode a did:key Ed25519 public key (multicodec 0xed01 + base58btc)."""
    if not did.startswith("did:key:z"):
        raise ValueError("only did:key:z... identifiers are supported")
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    n = 0
    for char in did[len("did:key:z"):]:
        if char not in alphabet:
            raise ValueError("invalid base58btc DID")
        n = n * 58 + alphabet.index(char)
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big")
    # Base58btc drops leading zero bytes; multicodec Ed25519 keys begin 0xed 0x01.
    if len(raw) != 34 or raw[:2] != b"\xed\x01":
        raise ValueError("DID is not an Ed25519 did:key")
    return Ed25519PublicKey.from_public_bytes(raw[2:])


def signing_payload(room: str, nonce: int, text: str) -> bytes:
    """The exact byte payload signed by Technocore: room|nonce|normalized-text."""
    return f"{room}|{nonce}|{normalize_text(text)}".encode("utf-8")


def verify_signature(did: str, signature: str, room: str, nonce: int, text: str) -> bool:
    key = public_key_from_did(did)
    try:
        key.verify(_b64url_decode(signature), signing_payload(room, nonce, text))
        return True
    except Exception:
        return False


def canonical_receipt(did: str, room: str, nonce: int, text: str, signature: str) -> dict[str, Any]:
    """Return a stable, JSON-serializable evidence record."""
    normalized = normalize_text(text)
    return {
        "version": 1,
        "type": "technocore-receipt",
        "did": did,
        "room": room,
        "nonce": nonce,
        "text": normalized,
        "signature": signature,
    }


def receipt_bytes(receipt: dict[str, Any]) -> bytes:
    return (json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
