"""Portable receipts for signed content."""

from hashlib import sha256
import json


def make_receipt(*, did: str, payload: str, signature: str, kind: str = "technocore-message") -> dict[str, str]:
    """Return a stable, JSON-friendly receipt without handling private keys."""
    digest = sha256(payload.encode("utf-8")).hexdigest()
    return {
        "version": "1",
        "kind": kind,
        "did": did,
        "sha256": digest,
        "signature": signature,
    }


def canonical_json(receipt: dict[str, str]) -> str:
    """Serialize a receipt deterministically for storage or signing elsewhere."""
    return json.dumps(receipt, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
