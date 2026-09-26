from typing import Any, Literal

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    step: int
    tool: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    success: bool
    data: Any = None
    error: str | None = None


class Observation(BaseModel):
    step: int
    tool: str
    result: ToolResult


class ToolDecision(BaseModel):
    action: Literal["tool"]
    tool: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class FinishDecision(BaseModel):
    action: Literal["finish"]
    answer: str


class AgentState(BaseModel):
    goal: str

    plan: list[str] = Field(default_factory=list)

    current_step: int = 0

    messages: list[dict[str, Any]] = Field(default_factory=list)

    tool_calls: list[ToolCall] = Field(default_factory=list)

    observations: list[Observation] = Field(default_factory=list)

    errors: list[str] = Field(default_factory=list)

    status: Literal[
        "running",
        "completed",
        "failed",
        "max_steps",
    ] = "running"

    final_answer: str | None = None

    steps: int = 0