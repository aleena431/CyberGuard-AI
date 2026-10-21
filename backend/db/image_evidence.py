from backend.db.database import get_db_connection


def initialize_image_evidence_table() -> None:
    """Create the table for permanently retained image metadata."""
    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS image_evidence (
                id BIGSERIAL PRIMARY KEY,
                stored_filename TEXT NOT NULL UNIQUE,
                original_filename TEXT NOT NULL,
                image_format TEXT NOT NULL,
                width INTEGER NOT NULL,
                height INTEGER NOT NULL,
                size_bytes BIGINT NOT NULL,
                incident_id BIGINT,
                uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                expires_at TIMESTAMPTZ NULL
            )
            """
        )

        # Support databases created with the previous 30-day design.
        connection.execute(
            """
            ALTER TABLE image_evidence
            ALTER COLUMN expires_at DROP NOT NULL
            """
        )


def register_image_evidence(
    stored_filename: str,
    original_filename: str,
    image_format: str,
    width: int,
    height: int,
    size_bytes: int,
    incident_id: int | None = None,
) -> dict:
    """Save image metadata without setting an automatic expiry date."""
    with get_db_connection() as connection:
        row = connection.execute(
            """
            INSERT INTO image_evidence (
                stored_filename,
                original_filename,
                image_format,
                width,
                height,
                size_bytes,
                incident_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, uploaded_at
            """,
            (
                stored_filename,
                original_filename,
                image_format,
                width,
                height,
                size_bytes,
                incident_id,
            ),
        ).fetchone()

    return {
        "id": row[0],
        "uploaded_at": row[1].isoformat(),
    }

def link_evidence_to_incident(evidence_id: int, incident_id: int) -> None:
    """Link saved image evidence to an existing incident."""
    with get_db_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE image_evidence
            SET incident_id = %s
            WHERE id = %s
            RETURNING id
            """,
            (incident_id, evidence_id),
        )

        if cursor.fetchone() is None:
            raise ValueError(
                f"Image evidence with ID {evidence_id} was not found."
            )
