
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from backend.app.rag.investigator import investigate


class InvestigationState(TypedDict):
    question: str
    top_k: int
    result: dict


def run_investigation(state: InvestigationState) -> dict:
    """Run the existing RAG and LLM investigation."""
    result = investigate(
        state["question"],
        top_k=state["top_k"],
    )

    return {"result": result}


builder = StateGraph(InvestigationState)

builder.add_node("investigate", run_investigation)

builder.add_edge(START, "investigate")
builder.add_edge("investigate", END)

investigation_graph = builder.compile()


def run_graph(question: str, top_k: int = 3) -> dict:
    """Execute the investigation workflow."""
    result = investigation_graph.invoke(
        {
            "question": question,
            "top_k": top_k,
            "result": {},
        }
    )

    return result["result"]
