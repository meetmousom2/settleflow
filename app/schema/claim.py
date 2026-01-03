from enum import Enum

from pydantic import BaseModel, Field


# 1. Restrict the statuses allowed in the system
class ClaimStatus(str, Enum):
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING_EVIDENCE = "pending_evidence"


# 2. Structure the logs so they are always [NodeName]: [Text]
class AnalysisLog(BaseModel):
    node: str = Field(description="Name of the agent/node that created this log")
    message: str = Field(description="The actual reasoning or observation")
    timestamp: str = Field(description="ISO timestamp of the entry")


# 3. Define the structured decision
class ClaimDecision(BaseModel):
    status: ClaimStatus
    amount_approved: float = Field(default=0.0)
    rejection_reason: str | None = None
