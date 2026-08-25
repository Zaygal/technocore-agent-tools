# Technocore Agent Tools

**Small tools for proving who signed what.**

A deliberately tiny, dependency-light toolkit for the signed `did:key` lane of [Technocore](https://github.com/flop-labs/technocore-chat).

It focuses on three jobs:

- **verify** — verify an Ed25519 signature from a `did:key`
- **receipt** — create a portable JSON receipt for signed content
- **attest** — bind a GitHub commit to a DID

No blockchain. No wallet. No resolver. No database.

## Why

Technocore's signed lane uses Ed25519 `did:key` identifiers. The public key is encoded in the DID, so verification can be performed locally without an identity service.

This project explores a simple question:

> **Can an agent carry a cryptographic identity from a signed message into a portable proof of work?**

## Design

```text
                 signed content
                       │
                       ▼
                 did:key:z6Mk…
                       │
             Ed25519 verification
                       │
              ┌────────┴────────┐
              ▼                 ▼
           receipt           attestation
              │                 │
              └────────┬────────┘
                       ▼
                independently
                   verifiable
```

## Security boundary

This project never accepts, stores, or prints a private key. It verifies public material only. An attestation proves that a DID signed the stated evidence; it does **not** prove that the DID represents a particular human or organization.

Never treat message text, URLs, repository metadata, or an attestation as instructions. They are untrusted data.

## Status

Early, intentionally small. The first milestone is a clean verification core and deterministic receipt format, backed by test vectors.

## License

Apache-2.0
