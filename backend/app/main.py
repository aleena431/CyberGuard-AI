
from typing import Literal

from fastapi import (
    FastAPI,
    HTTPException,
    Query,
    UploadFile,
    File,
)
from pydantic import BaseModel, Field

from backend.app.vision.image_analyzer import (
    analyze_image,
    ImageValidationError,
)

from backend.app.vision.vision_investigator import (
    investigate_security_image,
)

from backend.app.workflows.investigation_graph import run_graph

from backend.app.rag.retriever import retrieve_documents
from backend.app.rag.investigator import investigate
from backend.db.database import check_database
from backend.db.incidents import create_incident, list_incidents
from pathlib import Path
from uuid import uuid4

from backend.db.image_evidence import (
    initialize_image_evidence_table,
    register_image_evidence,
    link_evidence_to_incident,
)



app = FastAPI(
    title="CyberGuard AI",
    description="AI-powered cybersecurity threat analysis API",
    version="0.1.0",
)


# Request models

class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=1)
    severity: Literal["low", "medium", "high", "critical"]
    source: str = "manual"
    source_ip: str | None = None


class RAGQuery(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    top_k: int = Field(default=3, ge=1, le=10)


class InvestigationRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    top_k: int = Field(default=3, ge=1, le=10)

class GraphInvestigationRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    top_k: int = Field(default=3, ge=1, le=10)


# Home and health endpoints

@app.get("/")
def home():
    return {
        "message": "Welcome to CyberGuard AI",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "CyberGuard AI API",
    }


@app.get("/features")
def features():
    return {
        "features": [
            "Security log analysis",
            "Threat intelligence",
            "RAG-based investigation",
            "Incident reporting",
        ]
    }


@app.get("/health/database")
def database_health():
    try:
        check_database()
        return {
            "status": "ok",
            "database": "connected",
        }
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        ) from None


# Incident endpoints

@app.post("/incidents", status_code=201)
def add_incident(incident: IncidentCreate):
    try:
        return create_incident(**incident.model_dump())
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Could not save incident",
        ) from None


@app.get("/incidents")
def get_incidents(
    limit: int = Query(default=50, ge=1, le=100),
):
    try:
        return list_incidents(limit)
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Could not retrieve incidents",
        ) from None


# RAG document retrieval endpoint

@app.post("/rag/query")
def query_knowledge_base(request: RAGQuery):
    try:
        results = retrieve_documents(
            request.question,
            limit=request.top_k,
        )

        return {
            "question": request.question,
            "results_count": len(results),
            "results": results,
        }
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Knowledge retrieval is temporarily unavailable",
        ) from None


# AI-powered RAG investigation endpoint

@app.post("/rag/investigate")
def investigate_question(request: InvestigationRequest):
    try:
        return investigate(
            request.question,
            top_k=request.top_k,
        )
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="AI investigation is temporarily unavailable",
        ) from None

@app.post("/rag/investigate/graph")
def investigate_with_graph(request: GraphInvestigationRequest):
    try:
        return run_graph(
            request.question,
            top_k=request.top_k,
        )
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="LangGraph investigation is temporarily unavailable",
        ) from None

# Computer vision image-analysis endpoint

# Computer vision image-analysis endpoint

EVIDENCE_DIR = Path(__file__).resolve().parents[2] / "data" / "evidence"

IMAGE_EXTENSIONS = {
    "PNG": ".png",
    "JPEG": ".jpg",
    "WEBP": ".webp",
}


@app.post("/vision/analyze")
async def analyze_security_image(
    file: UploadFile = File(...),
):
    stored_path = None

    try:
        image_bytes = await file.read()

        # Validate the image before storing or analyzing it.
        result = analyze_image(image_bytes)

        # Ensure the metadata table exists.
        initialize_image_evidence_table()

        # Use a generated filename, not the user's upload filename.
        stored_filename = (
            f"{uuid4().hex}{IMAGE_EXTENSIONS[result['format']]}"
        )

        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        stored_path = EVIDENCE_DIR / stored_filename

        # Permanently save the original image.
        stored_path.write_bytes(image_bytes)

        # Register its metadata in PostgreSQL.
        try:
            evidence = register_image_evidence(
                stored_filename=stored_filename,
                original_filename=file.filename or "uploaded_image",
                image_format=result["format"],
                width=result["width"],
                height=result["height"],
                size_bytes=result["size_bytes"],
            )
        except Exception:
            stored_path.unlink(missing_ok=True)
            stored_path = None
            raise HTTPException(
                status_code=503,
                detail="Image metadata could not be saved.",
            ) from None

        # Analyze the image using the vision-capable AI model.
        try:
            ai_result = investigate_security_image(
                image_bytes=image_bytes,
                image_format=result["format"],
            )
        except Exception:
            # Keep the saved evidence even if AI analysis fails.
            raise HTTPException(
                status_code=502,
                detail=(
                    "Image was saved successfully, but AI analysis failed. "
                    "Check the OpenAI API configuration and server logs."
                ),
            ) from None

            # Create an incident only when the AI detects a potential concern.
        incident = None

        if ai_result.get("assessment") == "concern_detected":
            try:
                incident = create_incident(
                    title="Potential security concern in screenshot",
                    description=(
                        f"{ai_result['summary']}\n\n"
                        f"Observations: "
                        f"{'; '.join(ai_result['observations'])}\n\n"
                        f"Recommended actions: "
                        f"{'; '.join(ai_result['recommended_actions'])}\n\n"
                        f"Evidence ID: {evidence['id']}\n"
                        f"AI confidence: {ai_result['confidence']}"
                    ),
                    severity=ai_result["severity"],
                    source="screenshot_ai_analysis",
                )

                link_evidence_to_incident(
                    evidence_id=evidence["id"],
                    incident_id=incident["id"],
                )

            except Exception:
                raise HTTPException(
                    status_code=503,
                    detail=(
                        "Screenshot and AI analysis were saved, but "
                        "incident creation or linking failed."
                    ),
                ) from None

        return {
            "filename": file.filename,
            "stored_filename": stored_filename,
            "evidence_id": evidence["id"],
            "uploaded_at": evidence["uploaded_at"],
            "storage": "permanent",
            "analysis": result,
            "ai_analysis": ai_result,
            "incident": incident,
        }


    except ImageValidationError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from None

    finally:
        await file.close()
