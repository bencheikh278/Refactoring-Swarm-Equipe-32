import os
from src.utils.logger import log_experiment, ActionType


class AuditorAgent:

    def __init__(self, client):
        self.name = "AuditorAgent"
        self.client = client

        # ✅ Load prompt from src/prompts
        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        prompt_path = os.path.join(
            base_dir,
            "prompts",
            "auditeur_prompts.md"
        )

        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt not found: {prompt_path}")

        with open(prompt_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def analyze(self, target_dir):

        full_code = ""

        for root, _, files in os.walk(target_dir):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)

                    with open(filepath, "r", encoding="utf-8") as f:
                        full_code += f"\n\n# FILE: {file}\n"
                        full_code += f.read()

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # ✅ GROQ MODEL
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": full_code}
            ]
        )

        result = response.choices[0].message.content

        log_experiment(
            agent_name="Auditeur",
            model_used="groq",
            action=ActionType.ANALYSIS,
            details={
                "input_prompt": full_code,
                "output_response": result
            },
            status="SUCCESS"
        )

        return result