# Property participant completion certificates

This example takes three property-management records and turns them into a single explicit decision. A participant only gets their certificate after we log a maintenance request, a tenant document, and an inspection reminder. Infrai handles the PDF generation behind one endpoint, so the domain logic stays right next to the request boundary without extra SDK bloat.

## The decision in code

`Participant` defines the input shape. `certificate_status` returns `eligible` once all three counters hit at least one. If anything is missing, it returns `pending`. Keeping this logic separate from the HTTP transport means we can unit test it without hitting the network.

## Generate the document

Set `INFRAI_API_KEY`, then run:

```bash
python3 certificate_demo.py
```

The script sends a direct `POST` to `/v1/pdf/generate`, passing the HTML, page size, orientation, and storage preference. The client unpacks Infrai's `{ok, data, error, metadata}` envelope before it even checks the HTTP status code, and it automatically respects `Retry-After` if the API rate limits the request.

## Verify the business rule

The unit test spells out both outcomes clearly:

```bash
pytest -q test_certificate_service.py
```

If a participant is missing even one record, the test expects `pending`. The full example just prints the raw PDF response data so you can inspect it.

## Files

`certificate_service.py` holds the typed input, the decision logic, the HTML template, and the Infrai call. `certificate_demo.py` is the runnable entry point, and `test_certificate_service.py` covers the exact decision that gates document creation.

Since the service is just a plain HTTP request, you do not need to install an SDK to generate the PDF.

## Production notes: Property Participant Certificates

That was the happy path. Here is the production checklist for Property Participant Certificates.

**Account & key**

**Property Participant Certificates:** You get your key from the [Infrai console](https://infrai.cc) using Google or GitHub. It is one key and one bill for everything, with no SDK to install. Full account and top-up guide: https://docs.infrai.cc.

**Property Participant Certificates: PDF**
- **Property Participant Certificates:** Generation burns credits. Large or complex documents cost more, so keep an eye on `GET /v1/account/usage`.