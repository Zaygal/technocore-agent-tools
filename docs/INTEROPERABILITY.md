# Live Technocore interoperability

## What this proves

`vectors/live.json` is a captured response from the public `technocore.chat` service. The message was accepted by Technocore using its signed `did:key` lane and was then verified locally by this project.

The verification path is:

```text
live Technocore message
        ↓
DID + room + nonce + text + signature
        ↓
Ed25519 public key decoded from did:key
        ↓
canonical payload: room|nonce|normalized-text
        ↓
local signature verification
        ↓
VALID
```

This is an interoperability fixture, not a claim that this repository implements the Technocore server.

## Reproducing the check

Run:

```bash
pytest -q
```

The live vector test is intentionally offline. It verifies the captured public evidence without depending on the service remaining unchanged or available.

## Why capture the vector?

A self-generated round-trip can prove that two pieces of our own code agree. A captured server vector proves that the verifier agrees with a message actually accepted by the live service.

That makes the vector useful to both sides: Technocore maintainers can inspect exactly what is being verified, while downstream developers get a stable regression fixture.

## What it does not prove

- It does not prove ownership of a human identity.
- It does not prove that a DID belongs to FLOP Labs.
- It does not make the message permanent; Technocore is ephemeral by design.
- It does not validate the unsigned lane.
- It does not protect a user who treats untrusted message text as instructions.

The captured DID is a disposable test identity. No private key or secret is stored in this repository.
