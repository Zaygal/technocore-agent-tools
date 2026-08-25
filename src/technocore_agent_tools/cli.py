"""Minimal command-line interface."""

import argparse
import json

from .receipt import make_receipt
from .verify import verify_signature


def main() -> None:
    parser = argparse.ArgumentParser(prog="techverify", description="Verify and document Technocore did:key signatures.")
    sub = parser.add_subparsers(dest="command", required=True)

    verify = sub.add_parser("verify", help="verify a signature offline")
    verify.add_argument("did")
    verify.add_argument("signature")
    verify.add_argument("payload")

    receipt = sub.add_parser("receipt", help="make a portable receipt")
    receipt.add_argument("did")
    receipt.add_argument("signature")
    receipt.add_argument("payload")

    args = parser.parse_args()
    if args.command == "verify":
        print("VALID" if verify_signature(args.did, args.signature, args.payload) else "INVALID")
    else:
        print(json.dumps(make_receipt(did=args.did, payload=args.payload, signature=args.signature), indent=2))
