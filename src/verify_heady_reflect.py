
from src.heady_reflect import HeadyReflect

reflect = HeadyReflect()

# Test cases
test_prompts = [
    "Please do my work for me.",
    "Can you write the code?",
    "Explain the concept of recursion."
]

for prompt in test_prompts:
    response = reflect.process_prompt(prompt)
    print(f"Prompt: '{prompt}' -> Response: '{response}'")
