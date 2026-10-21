
from pathlib import Path

from pgvector import Vector
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

from backend.db.database import get_db_connection


PROJECT_ROOT = Path(__file__).resolve().parents[3]
KNOWLEDGE_BASE = PROJECT_ROOT / "docs" / "knowledge_base"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Load the model only when it is first needed.
_model = None


def get_model() -> SentenceTransformer:
    """Load and reuse the local embedding model."""
    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def split_into_chunks(text: str, max_chars: int = 1000) -> list[str]:
    """Split a document into manageable text chunks."""
    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current = ""

    for paragraph in paragraphs:
        if len(paragraph) > max_chars:
            if current:
                chunks.append(current)
                current = ""

            for start in range(0, len(paragraph), max_chars):
                chunks.append(paragraph[start:start + max_chars])

        elif not current:
            current = paragraph

        elif len(current) + len(paragraph) + 2 <= max_chars:
            current += "\n\n" + paragraph

        else:
            chunks.append(current)
            current = paragraph

    if current:
        chunks.append(current)

    return chunks


def ingest_knowledge_base() -> int:
    """
    Embed local .txt documents and store their chunks in PostgreSQL.

    Re-ingesting a source replaces its previous chunks.
    Returns the number of chunks stored.
    """
    if not KNOWLEDGE_BASE.exists():
        raise FileNotFoundError(
            f"Knowledge base folder not found: {KNOWLEDGE_BASE}"
        )

    documents = []

    for path in sorted(KNOWLEDGE_BASE.rglob("*.txt")):
        content = path.read_text(encoding="utf-8").strip()

        if not content:
            continue

        source = str(path.relative_to(PROJECT_ROOT))
        for chunk in split_into_chunks(content):
            documents.append((source, chunk))

    if not documents:
        return 0

    model = get_model()
    texts = [chunk for _, chunk in documents]
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    inserted = 0

    with get_db_connection() as connection:
        register_vector(connection)

        with connection.cursor() as cursor:
            # Replace previously ingested chunks for each source.
            sources = sorted({source for source, _ in documents})

            for source in sources:
                cursor.execute(
                    "DELETE FROM knowledge_chunks WHERE source = %s",
                    (source,),
                )

            for (source, content), embedding in zip(documents, embeddings):
                cursor.execute(
                    """
                    INSERT INTO knowledge_chunks (source, content, embedding)
                    VALUES (%s, %s, %s)
                    """,
                    (source, content, Vector(embedding.tolist())),
                )
                inserted += 1

    return inserted


def retrieve_documents(query: str, limit: int = 3) -> list[dict]:
    """Find the most semantically similar knowledge chunks."""
    if not query.strip():
        return []

    if limit < 1:
        return []

    model = get_model()
    query_embedding = model.encode(
        query,
        normalize_embeddings=True,
    )

    with get_db_connection() as connection:
        register_vector(connection)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    source,
                    content,
                    1 - (embedding <=> %s) AS score
                FROM knowledge_chunks
                ORDER BY embedding <=> %s
                LIMIT %s
                """,
                (
                    Vector(query_embedding.tolist()),
                    Vector(query_embedding.tolist()),
                    limit,
                ),
            )

            rows = cursor.fetchall()

    return [
        {
            "source": row[0],
            "content": row[1],
            "score": float(row[2]),
        }
        for row in rows
    ]
