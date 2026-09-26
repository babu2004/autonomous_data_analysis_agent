from agent.state import (
    AgentState,
    FinishDecision,
    ToolDecision,
    ToolResult,
)


def test_agent_state():

    state = AgentState(
        goal="Analyze sales.csv and find the best region."
    )

    assert state.goal == "Analyze sales.csv and find the best region."
    assert state.status == "running"
    assert state.steps == 0
    assert state.plan == []


def test_tool_decision():

    decision = ToolDecision(
        action="tool",
        tool="inspect_dataset",
        arguments={}
    )

    assert decision.action == "tool"
    assert decision.tool == "inspect_dataset"


def test_finish_decision():

    decision = FinishDecision(
        action="finish",
        answer="West is the best-performing region."
    )

    assert decision.action == "finish"


def test_tool_result_success():

    result = ToolResult(
        success=True,
        data={"rows": 1250}
    )

    assert result.success is True
    assert result.data["rows"] == 1250


def test_tool_result_error():

    result = ToolResult(
        success=False,
        error="File not found"
    )

    assert result.success is False
    assert result.error == "File not found"