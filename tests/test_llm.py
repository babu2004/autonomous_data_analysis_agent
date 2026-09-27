from llm.grok_provider import GrokProvider


def test_grok_provider():

    provider = GrokProvider()

    response = provider.generate(
        [
            {
                "role": "user",
                "content": "Reply with exactly: LLM connection works.",
            }
        ]
    )

    assert response
    assert response.choices
    assert response.choices[0].message.content

    print("\nLLM RESPONSE:")
    print(response.choices[0].message.content)