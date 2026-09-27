TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "inspect_dataset",
            "description": "Inspect a CSV dataset and return its structure, columns, data types, row count, and missing values.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the CSV file."
                    }
                },
                "required": ["file_path"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "dataset_statistics",
            "description": "Calculate descriptive statistics for numeric columns in a CSV dataset.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the CSV file."
                    }
                },
                "required": ["file_path"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "group_analysis",
            "description": (
                "Group a dataset by a categorical column and calculate "
                "the sum of a numeric metric for each group. "
                "Use this for questions such as which region or product "
                "has the highest total revenue."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the CSV file."
                    },
                    "group_by": {
                        "type": "string",
                        "description": (
                            "Column to group the data by, "
                            "such as region or product."
                        )
                    },
                    "metric": {
                        "type": "string",
                        "description": (
                            "Numeric column to aggregate, "
                            "such as revenue or quantity."
                        )
                    }
                },
                "required": [
                    "file_path",
                    "group_by",
                    "metric"
                ]
            }
        }
    }
]