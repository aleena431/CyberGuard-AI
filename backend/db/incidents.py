from psycopg.rows import dict_row

from backend.db.database import get_db_connection


def initialize_incidents_table() -> None:
    """Create the incidents table if it does not already exist."""
    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS incidents (
                id BIGSERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                severity TEXT NOT NULL
                    CHECK (severity IN ('low', 'medium', 'high', 'critical')),
                source TEXT NOT NULL DEFAULT 'manual',
                source_ip TEXT,
                status TEXT NOT NULL DEFAULT 'open'
                    CHECK (status IN ('open', 'investigating', 'resolved')),
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )


def create_incident(
    title: str,
    description: str,
    severity: str,
    source: str = "manual",
    source_ip: str | None = None,
) -> dict:
    """Reuse an existing matching open incident instead of duplicating it."""
    with get_db_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:

            if source_ip:
                cursor.execute(
                    """
                    SELECT id, title, description, severity, source,
                           source_ip, status, created_at
                    FROM incidents
                    WHERE title = %s
                      AND source = %s
                      AND source_ip = %s
                      AND status = 'open'
                    ORDER BY created_at DESC, id DESC
                    LIMIT 1
                    """,
                    (title, source, source_ip),
                )

                existing = cursor.fetchone()
                if existing:
                    return dict(existing)

            cursor.execute(
                """
                INSERT INTO incidents
                    (title, description, severity, source, source_ip)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, title, description, severity, source,
                          source_ip, status, created_at
                """,
                (title, description, severity, source, source_ip),
            )
            return dict(cursor.fetchone())



def list_incidents(limit: int = 50) -> list[dict]:
    """Return the newest incidents first."""
    with get_db_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT id, title, description, severity, source,
                       source_ip, status, created_at
                FROM incidents
                ORDER BY created_at DESC, id DESC
                LIMIT %s
                """,
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]
