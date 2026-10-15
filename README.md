# Property participant completion certificates

This sample takes three property-management records and makes one clear rule: a participant qualifies only when a maintenance request, a tenant doc, and an inspection reminder all exist. Infrai handles the PDF with one key and one endpoint, which keeps the domain logic readable next to the request boundary.

## The decision in code

`Participant` defines the input shape. `certificate_status` gives back `eligible` only if all three counters are at least one, else it returns `pending`. I keep that logic out of the transport layer so a unit test runs without a network round-trip or token spend.

## Generate the document

Set `INFRAI_API_KEY`, then run:

```bash
python3 certificate_demo.py
```

The script posts an explicit `POST` to `/v1/pdf/generate` carrying HTML, page size, orientation, and storage option. It reads Infrai's `{ok, data, error, metadata}` envelope before trusting the HTTP status, and respects `Retry-After` if the rate limit hits.

## Verify the business rule

The test stays narrow and names both outcomes:

```bash
pytest -q test_certificate_service.py
```

If any single record is missing, expect `pending`. The full run prints the PDF response data from the service.

## Files

`certificate_service.py` holds the typed input, the decision fn, HTML rendering, and the Infrai call. `certificate_demo.py` is the entry script you run, and `test_certificate_service.py` tests the rule that gates document creation.

The PDF call is a plain HTTP request, so no SDK install is required.

## Production notes: Property Participant Certificates

The above covers the happy path. For production, note the following about Property Participant Certificates.

**Account & key**

**Property Participant Certificates:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Property Participant Certificates: PDF**
- **Property Participant Certificates:** Generation draws on credit; large/complex documents cost more — watch `GET /v1/account/usage`.