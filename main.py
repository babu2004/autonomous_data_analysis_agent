from agent.agent import Agent


from llm.grok_provider import GrokProvider


def main():

    llm = GrokProvider()

    agent = Agent(
        llm=llm
    )

    state = agent.run(
        goal="Analyze this sales dataset and tell me which product made most profit.",
        file_path="data/sample_sales.csv",
    )

    print("\n[AGENT STATE]")
    print(f"Steps: {state.steps}")
    print(f"Tool calls: {len(state.tool_calls)}")
    print(f"Errors: {len(state.errors)}")
    print(f"Status: {state.status}")


if __name__ == "__main__":
    main()