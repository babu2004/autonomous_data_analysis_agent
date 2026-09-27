from typing import Any

from agent.state import ToolResult
from tools.registry import get_tool


def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> ToolResult:
    """Execute a registered tool safely."""

    tool = get_tool(tool_name)

    if tool is None:
        return ToolResult(
            success=False,
            error=f"Unknown tool: {tool_name}",
        )

    try:
        result = tool(**arguments)

        if isinstance(result, ToolResult):
            return result

        return ToolResult(
            success=True,
            data=result,
        )

    except Exception as exc:
        return ToolResult(
            success=False,
            error=f"Tool execution failed: {exc}",
        )