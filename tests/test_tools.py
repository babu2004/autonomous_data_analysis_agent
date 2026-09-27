from tools.executor import execute_tool
from tools.registry import list_tools


def test_inspect_dataset_is_registered():

    tools = list_tools()

    assert "inspect_dataset" in tools


def test_inspect_dataset():

    result = execute_tool(
        "inspect_dataset",
        {
            "file_path": "data/sample_sales.csv",
        },
    )

    assert result.success is True

    assert result.data["rows"] == 6

    assert "region" in result.data["columns"]


def test_unknown_tool():

    result = execute_tool(
        "does_not_exist",
        {},
    )

    assert result.success is False

    assert "Unknown tool" in result.error
    