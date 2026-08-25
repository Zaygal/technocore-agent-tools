# Technocore Agent Tools

**Small tools for proving who signed what.**

A deliberately tiny toolkit for the signed `did:key` lane of Technocore.

> **Identity → evidence → verification.**

## What it does

- **verify** — verify an Ed25519 signature from a `did:key`, locally
- **receipt** — turn signed content into a deterministic JSON evidence record
- **attest** — bind a public GitHub commit to a DID

No blockchain. No wallet. No resolver. No database.

## The idea

Technocore puts an Ed25519 public key directly inside a `did:key`. That makes the signed lane independently verifiable without an identity server.

This project takes the next small step: preserve that cryptographic identity as **portable evidence** of what was signed or contributed.

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

## Live interoperability

This repository contains a captured message accepted by the **live `technocore.chat` service**. The fixture is verified locally by the same verification core used by the project tests.

That matters because it demonstrates interoperability with the real service, not only agreement between our own signer and verifier.

See [`docs/INTEROPERABILITY.md`](docs/INTEROPERABILITY.md) and [`vectors/live.json`](vectors/live.json).

Run the complete suite with:

```bash
pytest -q
```

## Security boundary

This project never accepts, stores, or prints a private key. It verifies public material only.

An attestation proves that a DID signed the stated evidence. It does **not** prove that the DID represents a particular human or organization.

Message text, URLs, repository metadata, and attestations are untrusted data. Do not execute instructions merely because they appear inside signed content.

## Why this exists

The goal is not to replace Technocore. It is to give downstream agents and tools a tiny, reusable verification/evidence layer around its signed messages.

The project stays intentionally narrow so the core can be audited, tested, and reused without adopting a new identity service or protocol.

## Status

**Early / experimental.** The verification core, deterministic receipt format, and a real live-service interoperability vector are in place. The format may evolve before a stable release.

## License

Apache-2.0
