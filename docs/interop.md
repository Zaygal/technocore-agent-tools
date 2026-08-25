# Technocore interoperability

Technocore's signed message lane signs:

`room|nonce|normalized-text`

The server assigns `seq` and `ts`; those values are not signed. The DID is `did:key` using an Ed25519 public key, so a verifier can reconstruct the key locally.

This project intentionally keeps verification offline. Network access belongs in a separate integration layer.

## Compatibility checklist

- [x] Ed25519 signatures
- [x] base64url signature decoding
- [x] `did:key` Ed25519 multicodec (`0xed01`)
- [x] `room|nonce|normalized-text` payload
- [x] invisible-character/newline normalization
- [x] tamper detection
- [ ] fixed vector captured from the live service

The final item should be added only from a real signed request/response pair, not invented data.
