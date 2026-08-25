"""Create portable GitHub contribution attestations."""

from .receipt import make_receipt


def make_attestation(*, did: str, repository: str, commit: str, signature: str) -> dict[str, str]:
    """Describe an exact public commit as evidence signed by ``did``."""
    if not repository or not commit:
        raise ValueError("repository and commit are required")
    receipt = make_receipt(
        did=did,
        payload=f"github|{repository}|{commit}",
        signature=signature,
        kind="github-commit-attestation",
    )
    return {**receipt, "repository": repository, "commit": commit}
