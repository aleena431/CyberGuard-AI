
from backend.db.incidents import create_incident, list_incidents


def test_create_incident():
    """Verify that a new incident can be stored in PostgreSQL."""
    incident = create_incident(
        title="Automated test incident",
        description="Testing incident creation in CyberGuard AI.",
        severity="low",
        source="automated_test",
        source_ip="192.0.2.10",
    )

    assert incident["title"] == "Automated test incident"
    assert incident["severity"] == "low"
    assert incident["source_ip"] == "192.0.2.10"


def test_duplicate_open_incident_is_reused():
    """Verify repeated matching alerts reuse the same open incident."""
    first = create_incident(
        title="Duplicate prevention test",
        description="Testing duplicate prevention.",
        severity="high",
        source="automated_test",
        source_ip="192.0.2.20",
    )

    second = create_incident(
        title="Duplicate prevention test",
        description="Testing duplicate prevention.",
        severity="high",
        source="automated_test",
        source_ip="192.0.2.20",
    )

    assert first["id"] == second["id"]


def test_list_incidents():
    """Verify that the API's incident repository can list records."""
    incidents = list_incidents(limit=10)

    assert isinstance(incidents, list)
    assert len(incidents) <= 10
