async function analyzeDataset() {

const fileInput = document.getElementById("file");
const goalInput = document.getElementById("goal");
const button = document.getElementById("analyzeBtn");

const statusCard = document.getElementById("statusCard");
const resultCard = document.getElementById("resultCard");

const status = document.getElementById("status");
const stepsContainer = document.getElementById("steps");
const finalAnswer = document.getElementById("finalAnswer");


// -----------------------------
// Validate input
// -----------------------------

if (!fileInput.files.length) {
    alert("Please select a CSV file.");
    return;
}

if (!goalInput.value.trim()) {
    alert("Please enter an analysis goal.");
    return;
}


// -----------------------------
// Prepare UI
// -----------------------------

button.disabled = true;
button.textContent = "Analyzing...";

statusCard.classList.remove("hidden");
resultCard.classList.add("hidden");

stepsContainer.innerHTML = "";
finalAnswer.innerHTML = "";

status.textContent =
    "🤖 Agent is analyzing the dataset...";


// -----------------------------
// Build request
// -----------------------------

const formData = new FormData();

formData.append(
    "file",
    fileInput.files[0]
);

formData.append(
    "goal",
    goalInput.value.trim()
);


try {

    const response = await fetch(
        "/analyze",
        {
            method: "POST",
            body: formData
        }
    );


    const data = await response.json();


    // -----------------------------
    // Handle API errors
    // -----------------------------

    if (!response.ok || data.error) {

        throw new Error(
            data.error || "Analysis failed."
        );
    }


    // -----------------------------
    // Render agent status
    // -----------------------------

    status.textContent =
        `✅ Analysis completed in ${data.steps} agent steps.`;


    // -----------------------------
    // Render tool execution
    // -----------------------------

    renderSteps(data);


    // -----------------------------
    // Render Markdown final answer
    // -----------------------------

    if (data.final_answer) {

        finalAnswer.innerHTML =
            marked.parse(data.final_answer);

    } else {

        finalAnswer.innerHTML = `
            <p>
                No final answer was generated.
            </p>
        `;
    }


    resultCard.classList.remove("hidden");

} catch (error) {

    status.textContent =
        "❌ Analysis failed.";

    stepsContainer.innerHTML = `
        <div class="error">
            ${escapeHtml(error.message)}
        </div>
    `;

} finally {

    button.disabled = false;
    button.textContent = "Analyze Dataset";

}


}

/* =========================================================
Render Agent Steps
========================================================= */

function renderSteps(data) {


const container =
    document.getElementById("steps");

container.innerHTML = "";


if (!data.tool_calls || data.tool_calls.length === 0) {

    container.innerHTML = `
        <div class="empty-result">
            No tools were executed.
        </div>
    `;

    return;
}


data.tool_calls.forEach(
    (toolCall, index) => {

        const observation =
            data.observations?.[index];

        const step =
            document.createElement("div");

        step.className = "step";


        const toolName =
            toolCall.tool;

        const toolData =
            observation?.data;


        const summary =
            createToolSummary(
                toolName,
                toolData
            );


        const success =
            observation?.success !== false;


        step.innerHTML = `

            <div class="step-header">

                <div class="step-title">
                    Step ${toolCall.step}
                    → ${escapeHtml(toolName)}
                </div>

                <div class="success-badge">
                    ${success ? "✓ Success" : "✕ Failed"}
                </div>

            </div>


            <div class="tool-description">

                ${
                    success
                        ? "Tool executed successfully."
                        : "Tool execution failed."
                }

            </div>


            ${summary}


            <details>

                <summary>
                    View raw tool result
                </summary>


                <pre class="json-output">${escapeHtml(
                    JSON.stringify(
                        toolData ?? {},
                        null,
                        2
                    )
                )}</pre>

            </details>

        `;


        container.appendChild(step);
    }
);


}

/* =========================================================
Create Human-Friendly Tool Summary
========================================================= */

function createToolSummary(
toolName,
data
) {


// -----------------------------
// No result
// -----------------------------

if (
    !data ||
    typeof data !== "object" ||
    Object.keys(data).length === 0
) {

    return `
        <div class="empty-result">
            No structured result was returned by this tool.
        </div>
    `;
}


// -----------------------------
// Dataset inspection
// -----------------------------

if (
    toolName === "inspect_dataset"
) {

    return createInspectionSummary(data);
}


// -----------------------------
// Dataset statistics
// -----------------------------

if (
    toolName === "dataset_statistics"
) {

    return createStatisticsTable(data);
}


// -----------------------------
// Group analysis
// -----------------------------

if (
    toolName === "group_analysis"
) {

    return createGroupAnalysisTable(data);
}


// -----------------------------
// Generic fallback
// -----------------------------

return `
    <pre class="json-output">${escapeHtml(
        JSON.stringify(
            data,
            null,
            2
        )
    )}</pre>
`;


}

/* =========================================================
Dataset Inspection
========================================================= */

function createInspectionSummary(data) {


const rows =
    data.rows ?? 0;


const columns =
    Array.isArray(data.columns)
        ? data.columns.length
        : 0;


const missing =
    calculateMissingValues(
        data.missing_values
    );


const columnList =
    Array.isArray(data.columns)
        ? data.columns
            .map(
                column => `
                    <span class="column-tag">
                        ${escapeHtml(column)}
                    </span>
                `
            )
            .join("")
        : "-";


return `

    <div class="result-summary">

        <div class="summary-grid">


            <div class="summary-item">

                <div class="summary-label">
                    Rows
                </div>

                <div class="summary-value">
                    ${formatNumber(rows)}
                </div>

            </div>


            <div class="summary-item">

                <div class="summary-label">
                    Columns
                </div>

                <div class="summary-value">
                    ${formatNumber(columns)}
                </div>

            </div>


            <div class="summary-item">

                <div class="summary-label">
                    Missing Values
                </div>

                <div class="summary-value">
                    ${formatNumber(missing)}
                </div>

            </div>


        </div>

    </div>


    <div class="result-summary">

        <strong>
            Dataset Columns
        </strong>

        <div style="margin-top: 8px;">
            ${columnList}
        </div>

    </div>

`;

}

/* =========================================================
Dataset Statistics
========================================================= */

function createStatisticsTable(data) {


const columns =
    Object.keys(data);


if (!columns.length) {

    return `
        <div class="empty-result">
            No statistics were returned.
        </div>
    `;
}


/*
 * Find the statistic names from
 * the first numeric column.
 */

const statisticNames =
    Object.keys(
        data[columns[0]] || {}
    );


if (!statisticNames.length) {

    return `
        <div class="empty-result">
            No statistics were returned.
        </div>
    `;
}


let html = `

    <div class="result-summary">

        <strong>
            Numeric Statistics
        </strong>


        <table class="data-table">

            <thead>

                <tr>

                    <th>
                        Column
                    </th>

                    ${
                        statisticNames
                            .map(
                                name => `
                                    <th>
                                        ${escapeHtml(name)}
                                    </th>
                                `
                            )
                            .join("")
                    }

                </tr>

            </thead>


            <tbody>

`;


columns.forEach(
    column => {

        html += `

            <tr>

                <td>
                    <strong>
                        ${escapeHtml(column)}
                    </strong>
                </td>


                ${
                    statisticNames
                        .map(
                            name => `

                                <td>
                                    ${formatNumber(
                                        data[column]?.[name]
                                    )}
                                </td>

                            `
                        )
                        .join("")
                }

            </tr>

        `;
    }
);


html += `

            </tbody>

        </table>

    </div>

`;


return html;


}

/* =========================================================
Group Analysis
========================================================= */

function createGroupAnalysisTable(data) {

if (!data.results) {

    return `
        <div class="empty-result">
            No grouped analysis results were returned.
        </div>
    `;
}


const groups =
    Object.entries(
        data.results
    );


if (!groups.length) {

    return `
        <div class="empty-result">
            The grouped analysis returned no rows.
        </div>
    `;
}


const groupBy =
    data.group_by ?? "Group";


const metric =
    data.metric ?? "Value";


const aggregation =
    data.aggregation ?? "-";


return `

    <div class="result-summary">

        <div class="summary-grid">


            <div class="summary-item">

                <div class="summary-label">
                    Group By
                </div>

                <div class="summary-value">
                    ${escapeHtml(groupBy)}
                </div>

            </div>


            <div class="summary-item">

                <div class="summary-label">
                    Metric
                </div>

                <div class="summary-value">
                    ${escapeHtml(metric)}
                </div>

            </div>


            <div class="summary-item">

                <div class="summary-label">
                    Aggregation
                </div>

                <div class="summary-value">
                    ${escapeHtml(aggregation)}
                </div>

            </div>


        </div>

    </div>


    <div class="result-summary">

        <table class="data-table">

            <thead>

                <tr>

                    <th>
                        ${escapeHtml(groupBy)}
                    </th>

                    <th>
                        ${escapeHtml(metric)}
                    </th>

                </tr>

            </thead>


            <tbody>

                ${
                    groups
                        .map(
                            ([group, value]) => `

                                <tr>

                                    <td>
                                        ${escapeHtml(group)}
                                    </td>

                                    <td>
                                        <strong>
                                            ${formatNumber(value)}
                                        </strong>
                                    </td>

                                </tr>

                            `
                        )
                        .join("")
                }

            </tbody>

        </table>

    </div>

`;


}

/* =========================================================
Helper: Calculate Missing Values
========================================================= */

function calculateMissingValues(
values
) {


if (!values) {
    return 0;
}


return Object.values(values)
    .reduce(
        (
            total,
            value
        ) => {

            return total +
                Number(value || 0);

        },
        0
    );


}

/* =========================================================
Helper: Format Numbers
========================================================= */

function formatNumber(value) {


if (
    value === null ||
    value === undefined ||
    value === ""
) {

    return "-";
}


if (
    typeof value === "number" &&
    Number.isFinite(value)
) {

    return value.toLocaleString(
        undefined,
        {
            maximumFractionDigits: 2
        }
    );
}


return escapeHtml(value);


}

/* =========================================================
Helper: Escape HTML
========================================================= */

function escapeHtml(value) {


return String(value)
    .replace(
        /&/g,
        "&amp;"
    )
    .replace(
        /</g,
        "&lt;"
    )
    .replace(
        />/g,
        "&gt;"
    )
    .replace(
        /"/g,
        "&quot;"
    )
    .replace(
        /'/g,
        "&#039;"
    );


}
