import os
from src.utils.file_tools import read_file
from src.utils.logger import log_experiment, ActionType


class FixerAgent:

    def __init__(self, client):
        self.name = "FixerAgent"
        self.client = client

        # ✅ Load prompt safely
        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        prompt_path = os.path.join(
            base_dir,
            "prompts",
            "correcteur_prompts.md"
        )

        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt not found: {prompt_path}")

        with open(prompt_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def fix(self, target_dir, filename, issues=None):

        filepath = os.path.join(target_dir, filename)

        if not os.path.exists(filepath):
            print(f"⚠ File not found: {filepath}")
            return False

        code = read_file(filepath)
        error_output = issues if issues else ""

        full_prompt = f"""
{self.system_prompt}

Issues:
{error_output}

Code:
{code}

Return ONLY fixed full Python file.
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # ✅ GROQ MODEL
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": full_prompt}
            ]
        )

        fixed_code = response.choices[0].message.content

        # Remove markdown if model returns it
        if fixed_code.startswith("```"):
            fixed_code = "\n".join(fixed_code.split("\n")[1:-1])

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(fixed_code)

        log_experiment(
            agent_name="Correcteur",
            model_used="groq",
            action=ActionType.FIX,
            details={
                "input_prompt": full_prompt,
                "output_response": fixed_code
            },
            status="SUCCESS"
        )

        return True