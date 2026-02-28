import os
from src.utils.logger import log_experiment, ActionType


class AuditorAgent:

    def __init__(self, client):
        self.name = "AuditorAgent"
        self.client = client

    def analyze(self, target_dir):
        """Analyse tous les fichiers Python du dossier cible."""

        full_code = ""

        for root, _, files in os.walk(target_dir):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r") as f:
                        full_code += f"\n\n# FILE: {file}\n"
                        full_code += f.read()

        with open("prompts/auditeur_prompts.md", "r") as f:
            prompt_template = f.read()

        full_prompt = prompt_template + "\n\nVoici le code :\n" + full_code

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": full_prompt}]
        )

        result = response.choices[0].message.content

        log_experiment(
            agent_name="Auditeur",
            model_used="groq",
            action=ActionType.ANALYSIS,
            details={
                "input_prompt": full_prompt,
                "output_response": result
            },
            status="SUCCESS"
        )

        return result