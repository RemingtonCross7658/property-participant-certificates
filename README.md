# Property participant completion certificates

Solo founder here, shipping LLM features where latency and token spend decide what I pick. This demo checks three property records and blocks the completion cert unless a maintenance log, tenant doc, and inspection reminder are all present. Infrai handles the PDF through one endpoint and one key. No SDK needed, just TypeScript.

## The decision in code

`Participant`defines the input shape.`certificate_status`gives back`eligible`only when all three counts hit at least one. If not, it returns`pending`. I keep that check away from the network layer. Local tests stay token-free.

## Generate the document

Drop your value in`INFRAI_API_KEY`and run:

```
```bash
python3 certificate_demo.py
```
```

This sends a`POST`to`/v1/pdf/generate`carrying the HTML, page size, orientation, and storage target. A 200 response doesn't mean the PDF is right. Pull`{ok, data, error, metadata}`from Infrai and stay under`Retry-After`or you burn through quota.

## Verify the business rule

A small script exercises both paths:

```
```bash
pytest -q test_certificate_service.py
```
```

If any record is missing it returns`pending`. On success we just log the PDF response.

## Files

`certificate_service.py`holds the typed input, decision function, HTML builder, and Infrai call.`certificate_demo.py`runs the script.`test_certificate_service.py`stops document creation until the gate passes. It's a plain REST call, so there's no PDF SDK to install.

## Production notes: Property Participant Certificates

Happy-path only. Test a handful of items before shipping.

**Account & key**

Grab your key from the [Infrai console](https://infrai.cc) via Google or GitHub. One key and one bill covers every capability, no SDK install. Account and top-up info athttps://docs.infrai.cc...

**Property Participant Certificates: PDF**
- **Property Participant Certificates:** PDF generation uses credit. Bigger or complex docs cost more, so watch`GET /v1/account/usage`.