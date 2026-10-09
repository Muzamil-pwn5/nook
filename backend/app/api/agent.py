from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.llm.conversation import AgentConversation
from app.llm.agent_runner import LLMAgentRunner


router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


llm_agent: LLMAgentRunner | None = None


def get_llm_agent() -> LLMAgentRunner:
    global llm_agent
    if llm_agent is None:
        llm_agent = LLMAgentRunner()
    return llm_agent


# Temporary session store.
#
# Structure:
#
# sessions = {
#     "session-uuid": {
#         "pending_approvals": {
#             "approval-uuid": {
#                 "conversation": ...,
#                 "pending_action": ...
#             }
#         }
#     }
# }
#
# This is intentionally in-memory for now.
# PostgreSQL/Redis persistence comes later.
sessions: dict[str, dict] = {}


def record_event(session: dict, event_type: str, label: str) -> None:
    now = datetime.now(timezone.utc)
    session["last_activity"] = now
    session["events"].append({"type": event_type, "label": label, "timestamp": now})
    session["events"] = session["events"][-50:]


class CreateSessionResponse(BaseModel):
    session_id: str


class AgentMessageRequest(BaseModel):
    session_id: str = Field(
        min_length=1,
        description="Unique identifier for the user's agent session.",
    )
    message: str = Field(
        min_length=1,
        description="Natural-language message for the agent.",
    )


def get_session(session_id: str) -> dict:
    session = sessions.get(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )

    return session


@router.post(
    "/session",
    response_model=CreateSessionResponse,
)
def create_session():
    """
    Create a new isolated agent session.
    """

    session_id = str(uuid4())

    sessions[session_id] = {
        "pending_approvals": {},
        "conversation": AgentConversation(),
        "created_at": datetime.now(timezone.utc),
        "last_activity": datetime.now(timezone.utc),
        "message_count": 0,
        "events": [],
    }

    return {
        "session_id": session_id,
    }


@router.post("/chat")
def chat_with_agent(
    request: AgentMessageRequest,
):
    """
    Send a message to a specific agent session.
    """

    session = get_session(
        request.session_id
    )
    session["message_count"] += 1
    record_event(session, "conversation", "Shopper conversation started")

    try:
        result = get_llm_agent().run(
            user_message=request.message,
            conversation=session["conversation"],
        )
        session["conversation"] = result["conversation"]

        if result["type"] == "approval_required":
            approval_id = str(uuid4())

            session["pending_approvals"][
                approval_id
            ] = {
                "conversation": result[
                    "conversation"
                ],
                "pending_action": result[
                    "pending_action"
                ],
            }
            record_event(
                session,
                "approval",
                f"Approval requested for {result['pending_action']['tool_name']}",
            )

            return {
                "agent": "llm",
                **{
                    key: value
                    for key, value in result.items()
                    if key != "conversation"
                },
                "approval_id": approval_id,
                "session_id": request.session_id,
            }

        return {
            "agent": "llm",
            "session_id": request.session_id,
            **{
                key: value
                for key, value in result.items()
                if key != "conversation"
            },
        }

    except Exception:
        return {
            "agent": "unavailable",
            "session_id": request.session_id,
            "success": False,
            "type": "provider_unavailable",
                "response": (
                    "The concierge is not connected to a live AI provider yet. "
                    "Please configure a supported provider (OpenAI, Groq, or Google Gemini) and try again."
                ),
        }


@router.post(
    "/session/{session_id}/approve-order/{approval_id}"
)
def approve_order(
    session_id: str,
    approval_id: str,
):
    """
    Approve one specific pending action belonging
    to one specific session.
    """

    session = get_session(
        session_id
    )

    pending = session["pending_approvals"].get(
        approval_id
    )

    if pending is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Approval request not found, "
                "expired, or already completed."
            ),
        )

    action = pending["pending_action"]
    record_event(
        session,
        "approval",
        f"Approval granted for {action['tool_name']}",
    )

    result = get_llm_agent().resume_after_approval(
        conversation=pending["conversation"],
        tool_call_id=action["call_id"],
        tool_name=action["tool_name"],
        arguments=action["arguments"],
    )
    session["conversation"] = result["conversation"]

    if result["success"]:
        del session["pending_approvals"][
            approval_id
        ]

    return {
        "agent": "llm",
        "session_id": session_id,
        "approval_id": approval_id,
        **{
            key: value
            for key, value in result.items()
            if key != "conversation"
        },
    }


@router.get(
    "/session/{session_id}"
)
def get_session_status(
    session_id: str,
):
    """
    Return safe session metadata.

    Does not expose the conversation or customer PII.
    """

    session = get_session(
        session_id
    )

    pending_approval_ids = list(
        session["pending_approvals"].keys()
    )

    return {
        "session_id": session_id,
        "pending_approval_count": len(
            pending_approval_ids
        ),
        "pending_approval_ids": (
            pending_approval_ids
        ),
    }


@router.get("/mode")
def get_agent_mode():
    return {
        "mode": "live_provider_required"
    }
