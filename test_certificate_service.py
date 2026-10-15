from certificate_service import Participant, certificate_status


def test_certificate_requires_all_three_property_tasks():
    ready = Participant("Amina Chen", 1, 1, 1)
    missing_reminder = Participant("Amina Chen", 1, 1, 0)
    assert certificate_status(ready) == "eligible"
    assert certificate_status(missing_reminder) == "pending"
