from enum import Enum


class ActionRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


TOOL_POLICIES = {
    "search_products": {
        "risk": ActionRisk.LOW,
        "requires_approval": False,
    },
    "check_inventory": {
        "risk": ActionRisk.LOW,
        "requires_approval": False,
    },
    "create_order": {
        "risk": ActionRisk.MEDIUM,
        "requires_approval": True,
    },
}


def get_tool_policy(tool_name: str) -> dict:
    policy = TOOL_POLICIES.get(tool_name)

    if policy is None:
        return {
            "allowed": False,
            "risk": ActionRisk.HIGH,
            "requires_approval": True,
            "reason": f"No policy exists for tool '{tool_name}'.",
        }

    return {
        "allowed": True,
        "risk": policy["risk"],
        "requires_approval": policy["requires_approval"],
        "reason": "Tool has a defined policy.",
    }


def is_tool_allowed(tool_name: str) -> bool:
    return tool_name in TOOL_POLICIES