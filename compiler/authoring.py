"""Hash-bound authoring: every authored step is written from an exact packet and checked against it."""

from kernel.canonical import ContractError, content_hash


class AuthorRequired(ContractError):
    """The pipeline reached an authored step with no document; `packet` is what the author writes from."""

    def __init__(self, step_id, packet):
        super().__init__("AUTHOR_REQUIRED", f"{step_id} needs an authored document for this packet", packet["packet_sha256"])
        self.step_id, self.packet = step_id, packet


class StepFailed(ContractError):
    """A step's checks failed; `findings` say why and `step_id` says where (the replan trigger routes from it)."""

    def __init__(self, step_id, findings):
        super().__init__("GATE_FAILED", f"{step_id} failed {len(findings)} check(s)", findings)
        self.step_id, self.findings = step_id, findings


class GateFailed(StepFailed):
    """An authored document failed its step's checks; findings go back to the author with the same packet."""

    def __init__(self, step_id, findings, packet):
        super().__init__(step_id, findings)
        self.packet = packet


def seal(packet):
    body = {key: value for key, value in packet.items() if key != "packet_sha256"}
    return {**body, "packet_sha256": "sha256:" + content_hash(body)}


def bind(packet, document):
    if document.get("packet_sha256") != packet["packet_sha256"]:
        raise ContractError("PACKET_MISMATCH", "The authored document was written for a different packet",
                            [document.get("packet_sha256"), packet["packet_sha256"]])


def record(step_id, packet, document):
    """Provenance entry for one authored document."""
    return {"step_id": step_id, "packet_sha256": packet["packet_sha256"], "document_sha256": "sha256:" + content_hash(document),
            "author": dict(document["author"]), "attempt": document["attempt"]}
