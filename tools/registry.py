from collections.abc import Callable
from typing import Any

from tools.csv_tools import (
    inspect_dataset,
    dataset_statistics,
    group_analysis,
)


ToolFunction = Callable[..., Any]


TOOL_REGISTRY: dict[str, ToolFunction] = {}


def register_tool(name: str, function: ToolFunction) -> None:
    """Register a tool under a specific name."""

    if name in TOOL_REGISTRY:
        raise ValueError(f"Tool already registered: {name}")

    TOOL_REGISTRY[name] = function


def get_tool(name: str) -> ToolFunction | None:
    """Return a registered tool."""

    return TOOL_REGISTRY.get(name)


def list_tools() -> list[str]:
    """Return all registered tool names."""

    return list(TOOL_REGISTRY.keys())


register_tool("inspect_dataset",inspect_dataset,)
register_tool("dataset_statistics", dataset_statistics)
register_tool("group_analysis", group_analysis)