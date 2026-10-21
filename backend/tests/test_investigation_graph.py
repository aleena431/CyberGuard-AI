
from backend.app.workflows.investigation_graph import run_graph


def test_run_graph_returns_investigation(monkeypatch):
    from backend.app.workflows import investigation_graph as workflow

    def fake_investigate(question, top_k=3):
        return {
            "question": question,
            "model": "test-model",
            "answer": "Review the authentication logs.",
            "sources": [],
        }

    monkeypatch.setattr(workflow, "investigate", fake_investigate)

    result = run_graph(
        "Investigate repeated login failures",
        top_k=3,
    )

    assert result["question"] == "Investigate repeated login failures"
    assert result["model"] == "test-model"
    assert "authentication logs" in result["answer"]
    assert result["sources"] == []
