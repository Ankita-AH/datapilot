import json
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

def add(a: float, b: float) -> float:
    return a + b

add_tool = {
    "type": "function",
    "name": "add",
    "description": "Adds two numbers together and returns the sum.",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {"type": "number", "description": "The first number"},
            "b": {"type": "number", "description": "The second number"},
        },
        "required": ["a", "b"],
    },
}
interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="What is 47 plus 89?",
    tools=[add_tool],
)

for step in interaction.steps:
    if step.type == "function_call":
        result = add(**step.arguments)
        print(f"Called {step.name}({step.arguments}) -> {result}")

        follow_up = client.interactions.create(
            model="gemini-3.8-flash",
            input=[{
                "type": "function_result",
                "name": step.name,
                "call_id": step.id,
                "result": [{"type": "text", "text": json.dumps(result)}],
            }],
            tools=[add_tool],
            previous_interaction_id=interaction.id,
        )
        print(follow_up.output_text)