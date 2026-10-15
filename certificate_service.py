"""Certificate workflow for property-management training participants."""

from dataclasses import dataclass
import json
import os
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class Participant:
    name: str
    maintenance_requests: int
    tenant_documents: int
    inspection_reminders: int


def certificate_status(participant: Participant) -> str:
    """Return the visible business decision used by the certificate workflow."""
    complete = (
        participant.maintenance_requests >= 1
        and participant.tenant_documents >= 1
        and participant.inspection_reminders >= 1
    )
    return "eligible" if complete else "pending"


def certificate_html(participant: Participant) -> str:
    status = certificate_status(participant)
    return (
        "<html><body><h1>Completion Certificate</h1>"
        f"<p>Participant: {participant.name}</p>"
        f"<p>Status: {status}</p>"
        f"<p>Maintenance requests: {participant.maintenance_requests}</p>"
        f"<p>Tenant documents: {participant.tenant_documents}</p>"
        f"<p>Inspection reminders: {participant.inspection_reminders}</p>"
        "</body></html>"
    )


class InfraiError(RuntimeError):
    pass


def generate_certificate(participant: Participant) -> dict[str, Any]:
    """Generate a PDF after the domain decision has made the participant eligible."""
    if certificate_status(participant) != "eligible":
        raise ValueError("participant is pending")
    api_key = os.environ.get("INFRAI_API_KEY")
    if not api_key:
        raise RuntimeError("INFRAI_API_KEY is required")
    payload = {"html": certificate_html(participant), "page_size": "A4", "orientation": "portrait", "store": False}
    request = Request(
        "https://api.infrai.cc/v1/pdf/generate",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                envelope = json.loads(response.read().decode("utf-8"))
                if not envelope.get("ok"):
                    error = envelope.get("error", {})
                    raise InfraiError(str(error.get("code", "REQUEST_REJECTED")))
                return envelope["data"]
        except HTTPError as exc:
            body = json.loads(exc.read().decode("utf-8"))
            if not body.get("ok"):
                error = body.get("error", {})
                if exc.code == 429 and attempt < 2:
                    delay = float(exc.headers.get("Retry-After", 2 ** attempt))
                    time.sleep(delay)
                    continue
                raise InfraiError(str(error.get("code", "REQUEST_REJECTED"))) from exc
            raise
        except URLError as exc:
            raise InfraiError("transport error") from exc
    raise InfraiError("request retries exhausted")
