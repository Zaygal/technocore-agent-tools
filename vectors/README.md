# Interoperability vectors

The test vector in `tests/test_protocol.py` signs the exact Technocore payload `room|nonce|normalized-text` with Ed25519 and verifies it from the derived `did:key`.

This directory is reserved for fixed cross-implementation vectors once the live service/client fixtures are captured.
