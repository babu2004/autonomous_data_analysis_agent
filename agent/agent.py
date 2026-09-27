import json

from agent.state import (
    AgentState,
    Observation,
    ToolCall,
)
from tools.definitions import TOOLS
from tools.executor import execute_tool


MAX_STEPS = 5


SYSTEM_PROMPT = """
You are an autonomous data analysis agent.

Your job is to analyze CSV datasets.

You should:

1. Understand the user's goal.
2. Decide which available tool is needed.
3. Call the appropriate tool.
4. Inspect the tool result.
5. Decide whether another tool is needed.
6. Return a clear final answer when enough information is available.

Use tools when they are necessary.
Do not invent tool results.
"""


class Agent:

    def __init__(self, llm):
        self.llm = llm

    def run(self, goal: str, file_path: str) -> AgentState:

        state = AgentState(goal=goal)

        state.plan = self._create_plan(goal)

        print("\n[PLAN]")

        for index, step in enumerate(state.plan, start=1):
            print(f"{index}. {step}")

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": (
                    f"Goal: {goal}\n\n"
                    f"Dataset path: {file_path}"
                ),
            },
        ]

        while state.status == "running":

            if state.steps >= MAX_STEPS:
                state.status = "max_steps"
                break

            response = self.llm.generate(
                messages=messages,
                tools=TOOLS,
            )

            message = response.choices[0].message

            print("\n[LLM RESPONSE]")

            if message.tool_calls:

                # Add assistant's tool-call message to conversation.
                messages.append(message.model_dump(exclude_none=True))

                for tool_call in message.tool_calls:

                    state.current_step += 1
                    state.steps += 1

                    tool_name = tool_call.function.name

                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                    print(f"\n[STEP {state.current_step}]")
                    print(f"→ {tool_name}")
                    print(f"Arguments: {arguments}")

                    state.tool_calls.append(
                        ToolCall(
                            step=state.current_step,
                            tool=tool_name,
                            arguments=arguments,
                            call_id=tool_call.id,
                        )
                    )

                    result = execute_tool(
                        tool_name,
                        arguments,
                    )

                    state.observations.append(
                        Observation(
                            step=state.current_step,
                            tool=tool_name,
                            result=result,
                        )
                    )

                    if result.success:

                        print("[OBSERVATION]")
                        print(result.data)

                        tool_content = json.dumps(
                            result.data,
                            default=str,
                        )

                    else:

                        print("[TOOL ERROR]")
                        print(result.error)

                        state.errors.append(
                            result.error or "Unknown tool error"
                        )

                        tool_content = json.dumps(
                            {
                                "error": result.error
                            }
                        )

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_content,
                        }
                    )

                continue

            # No tool call means the model is finished.
            state.final_answer = message.content or ""

            state.status = "completed"

            print("\n[FINAL]")
            print(state.final_answer)

            break

        return state

    def _create_plan(self, goal: str) -> list[str]:

        return [
            "Inspect the dataset",
            "Analyze the relevant data",
            "Generate the final findings",
        ]