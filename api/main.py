from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse

from agent.agent import Agent
from llm.grok_provider import GrokProvider


app = FastAPI(
    title="Autonomous Data Analysis Agent",
    description="An agentic AI system for analyzing CSV datasets.",
)

llm = GrokProvider()
agent = Agent(llm=llm)


@app.get("/")

def app_page():
    return FileResponse("static/index.html")

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    goal: str = Form(...),
):
    if not file.filename.lower().endswith(".csv"):
        return {
            "error": "Only CSV files are supported."
        }

    suffix = Path(file.filename).suffix

    with NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    ) as temp_file:

        content = await file.read()
        temp_file.write(content)
        file_path = temp_file.name

    try:
        state = agent.run(
            goal=goal,
            file_path=file_path,
        )

        return {
            "status": state.status,
            "goal": state.goal,
            "steps": state.steps,
            "tool_calls": [
                {
                    "step": call.step,
                    "tool": call.tool,
                    "arguments": call.arguments,
                    "call_id": call.call_id,
                }
                for call in state.tool_calls
            ],
            "observations": [
                {
                    "step": observation.step,
                    "tool": observation.tool,
                    "success": observation.result.success,
                    "data": observation.result.data,
                    "error": observation.result.error,
                }
                for observation in state.observations
            ],
            "errors": state.errors,
            "final_answer": state.final_answer,
        }

    finally:
        Path(file_path).unlink(missing_ok=True)  