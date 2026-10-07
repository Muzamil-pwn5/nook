from app.logging.audit import record_audit_event
from app.permissions.policies import get_tool_policy
from app.tools.registry import TOOL_REGISTRY


class AgentOrchestrator:
    def __init__(self):
        self.tools = TOOL_REGISTRY

    def list_tools(self) -> list[dict]:
        return [
            {
                "name": name,
                "description": details["description"],
                "policy": get_tool_policy(name),
            }
            for name, details in self.tools.items()
        ]

    def execute_tool(
        self,
        tool_name: str,
        arguments: dict,
        approved: bool = False,
    ) -> dict:
        if tool_name not in self.tools:
            result = {
                "success": False,
                "error": f"Tool '{tool_name}' is not available.",
            }

            record_audit_event(
                tool_name=tool_name,
                arguments=arguments,
                approved=approved,
                success=False,
                error=result["error"],
            )

            return result

        policy = get_tool_policy(tool_name)

        if not policy["allowed"]:
            result = {
                "success": False,
                "error": policy["reason"],
            }

            record_audit_event(
                tool_name=tool_name,
                arguments=arguments,
                approved=approved,
                success=False,
                error=result["error"],
            )

            return result

        if policy["requires_approval"] and not approved:
            result = {
                "success": False,
                "requires_approval": True,
                "risk": policy["risk"].value,
                "error": (
                    f"Tool '{tool_name}' requires approval "
                    "before execution."
                ),
            }

            record_audit_event(
                tool_name=tool_name,
                arguments=arguments,
                approved=approved,
                success=False,
                error=result["error"],
            )

            return result

        tool = self.tools[tool_name]["function"]

        try:
            tool_result = tool(**arguments)

            if isinstance(tool_result, dict):
                success = tool_result.get("success", True)
            else:
                success = True

            result = {
                "success": success,
                "tool": tool_name,
                "result": tool_result,
            }

            record_audit_event(
                tool_name=tool_name,
                arguments=arguments,
                approved=approved,
                success=success,
                result=tool_result,
                error=(
                    tool_result.get("error")
                    if isinstance(tool_result, dict) and not success
                    else None
                ),
            )

            return result

        except Exception as error:
            error_message = str(error)

            result = {
                "success": False,
                "tool": tool_name,
                "error": error_message,
            }

            record_audit_event(
                tool_name=tool_name,
                arguments=arguments,
                approved=approved,
                success=False,
                error=error_message,
            )

            return result