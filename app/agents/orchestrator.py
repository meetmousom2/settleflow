import operator
from datetime import datetime
from typing import Annotated, Literal

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from app.schema.claim import AnalysisLog, ClaimDecision, ClaimStatus


# --- 1. DEFINE THE STATE ---
class ClaimState(BaseModel):
    """
    The shared state for SettleFlow.
    Using Pydantic for automatic validation during node execution.
    """

    claim_id: str
    policy_text: str
    evidence_paths: list[str]

    # Reducer: Annotated + operator.add tells LangGraph to append to this list
    # instead of overwriting it, preserving our audit trail.
    analysis_logs: Annotated[list[AnalysisLog], operator.add] = []

    current_status: ClaimStatus = ClaimStatus.UNDER_REVIEW
    decision: ClaimDecision | None = None


# --- 2. DEFINE THE NODES (Agents) ---


def advocate_node(state: ClaimState):
    """
    Agent A: Tries to find evidence to SUPPORT the claim.
    """
    print(f"DEBUG: Advocate processing claim {state.claim_id}")

    # Logic: Call Gemini/DeepSeek to analyze policy vs evidence
    # response = call_llm(ADVOCATE_PROMPT, f"Policy: {state.policy_text}\nEvidence: {state.evidence_paths}")

    new_log = AnalysisLog(
        node="Advocate",
        message="Flight delay of 7 hours verified via boarding pass screenshot. Matches Article 4.1.",
        timestamp=datetime.now().isoformat(),
    )

    return {"analysis_logs": [new_log], "current_status": ClaimStatus.UNDER_REVIEW}


def auditor_node(state: ClaimState):
    """
    Agent B: Tries to find EXCLUSIONS or reasons to deny.
    """
    print(f"DEBUG: Auditor scrutinizing claim {state.claim_id}")

    new_log = AnalysisLog(
        node="Auditor",
        message="Cross-referencing Article 9: 'Strikes known 48h prior are excluded'. No strike info found yet.",
        timestamp=datetime.now().isoformat(),
    )

    return {"analysis_logs": [new_log]}


def judge_node(state: ClaimState):
    """
    Agent C: Resolves the debate into a final ClaimDecision.
    """
    print(f"DEBUG: Judge finalizing claim {state.claim_id}")

    # Final structured decision
    final_decision = ClaimDecision(
        status=ClaimStatus.APPROVED, amount_approved=150.00, rejection_reason=None
    )

    new_log = AnalysisLog(
        node="Judge",
        message=f"Final Verdict: {final_decision.status} for {final_decision.amount_approved}",
        timestamp=datetime.now().isoformat(),
    )

    return {
        "decision": final_decision,
        "current_status": ClaimStatus.APPROVED,
        "analysis_logs": [new_log],
    }


# --- 3. DEFINE CONDITIONAL LOGIC ---


def should_continue(state: ClaimState) -> Literal["continue", "end"]:
    """
    Logic to decide if we need more steps or if we can stop.
    """
    if state.current_status == ClaimStatus.APPROVED or state.current_status == ClaimStatus.REJECTED:
        return "end"
    return "continue"


# --- 4. CONSTRUCT THE GRAPH ---

builder = StateGraph(ClaimState)

# Add Nodes
builder.add_node("advocate", advocate_node)
builder.add_node("auditor", auditor_node)
builder.add_node("judge", judge_node)

# Define Flow
builder.add_edge(START, "advocate")
builder.add_edge("advocate", "auditor")
builder.add_edge("auditor", "judge")

# Conditional End (Optional example)
builder.add_edge("judge", END)

# Compile
# checkpointer=MemorySaver() can be added here later for 'time travel' debugging
orchestrator_app = builder.compile()
