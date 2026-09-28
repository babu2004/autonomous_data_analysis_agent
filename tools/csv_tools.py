from pathlib import Path

import pandas as pd

from agent.state import ToolResult


def inspect_dataset(file_path: str) -> ToolResult:
    """Inspect the structure of a CSV dataset."""

    try:
        path = Path(file_path)

        if not path.exists():
            return ToolResult(
                success=False,
                error=f"File not found: {file_path}",
            )

        if path.suffix.lower() != ".csv":
            return ToolResult(
                success=False,
                error="Only CSV files are supported.",
            )

        df = pd.read_csv(path)

        return ToolResult(
            success=True,
            data={
                "rows": len(df),
                "columns": list(df.columns),
                "dtypes": {
                    column: str(dtype)
                    for column, dtype in df.dtypes.items()
                },
                "missing_values": df.isnull().sum().to_dict(),
            },
        )

    except Exception as exc:
        return ToolResult(
            success=False,
            error=f"Failed to inspect dataset: {exc}",
        )

def dataset_statistics(file_path: str) -> ToolResult:
    try:
        path = Path(file_path)

        if not path.exists():
            return ToolResult(
                success=False,
                error=f"File not found: {file_path}",
            )

        if path.suffix.lower() != ".csv":
            return ToolResult(
                success=False,
                error="Only CSV files are supported.",
            )

        df = pd.read_csv(path)

        numeric_df = df.select_dtypes(include="number")

        if numeric_df.empty:
            return ToolResult(
                success=False,
                error="No numeric columns found in the dataset.",
            )

        statistics = numeric_df.describe().to_dict()

        return ToolResult(
            success=True,
            data=statistics,
        )

    except Exception as exc:
        return ToolResult(
            success=False,
            error=f"Failed to calculate statistics: {exc}",
        )

def group_analysis(
    file_path: str,
    group_by: str,
    metric: str,
) -> ToolResult:
    try:
        path = Path(file_path)

        if not path.exists():
            return ToolResult(
                success=False,
                error=f"File not found: {file_path}",
            )

        if path.suffix.lower() != ".csv":
            return ToolResult(
                success=False,
                error="Only CSV files are supported.",
            )

        df = pd.read_csv(path)

        if group_by not in df.columns:
            return ToolResult(
                success=False,
                error=f"Group column '{group_by}' not found in dataset.",
            )

        if metric not in df.columns:
            return ToolResult(
                success=False,
                error=f"Metric column '{metric}' not found in dataset.",
            )

        if not pd.api.types.is_numeric_dtype(df[metric]):
            return ToolResult(
                success=False,
                error=f"Metric '{metric}' must be numeric.",
            )

        grouped = (
            df.groupby(group_by)[metric]
            .sum()
            .sort_values(ascending=False)
        )

        # Keep the LLM context small while preserving
        # the complete calculation in Python.
        TOP_N = 5

        top_groups = grouped.head(TOP_N)

        result = {
            "group_by": group_by,
            "metric": metric,
            "aggregation": "sum",
            "total_groups": len(grouped),
            "top_groups": top_groups.to_dict(),
        }

        if not grouped.empty:
            result["highest_group"] = str(grouped.index[0])
            result["highest_value"] = grouped.iloc[0]

        return ToolResult(
            success=True,
            data=result,
        )

    except Exception as exc:
        return ToolResult(
            success=False,
            error=f"Failed to perform group analysis: {exc}",
        )