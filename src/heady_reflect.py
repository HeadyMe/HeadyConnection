
import re

class HeadyReflect:
    def __init__(self):
        self.patterns = [
            r"do my work",
            r"solve this for me",
            r"write the code"
        ]

    def process_prompt(self, prompt):
        for pattern in self.patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                return "Why do you need this work done? What are the underlying principles?"
        return prompt
