import json
from pathlib import Path

from techverify.protocol import verify_signature


VECTOR = json.loads((Path(__file__).parents[1] / "vectors" / "live.json").read_text())


def test_live_technocore_vector_verifies():
    assert VECTOR["source"] == "technocore.chat"
    assert VECTOR["kind"] == "live-signed-message"
    assert verify_signature(
        VECTOR["did"],
        VECTOR["signature"],
        VECTOR["room"],
        int(VECTOR["nonce"]),
        VECTOR["text"],
    )


def test_live_vector_fails_if_text_changes():
    assert not verify_signature(
        VECTOR["did"],
        VECTOR["signature"],
        VECTOR["room"],
        int(VECTOR["nonce"]),
        VECTOR["text"] + "!",
    )
