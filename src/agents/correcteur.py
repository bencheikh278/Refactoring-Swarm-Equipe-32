import os
from src.utils.logger import log_experiment, ActionType


class FixerAgent:

    def __init__(self, client):
        self.name = "FixerAgent"
        self.client = client

    def fix(self, target_dir, filename, issues=None):
        """Corrige un fichier Python selon les issues fournies."""

        filepath = os.path.join(target_dir, filename)

        if not os.path.exists(filepath):
            print(f"⚠️  Fichier introuvable : {filepath}")
            return False

        with open(filepath, "r") as f:
            code = f.read()

        with open("prompts/correcteur_prompts.md", "r") as f:
            system_prompt = f.read()

        full_prompt = f"""
{system_prompt}

Plan de correction :
{issues}

Code à corriger ({filename}) :
{code}

Retourne uniquement le code Python corrigé complet, sans balises markdown.
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": full_prompt}]
        )

        fixed_code = response.choices[0].message.content

        # Nettoyer les balises markdown si présentes
        if fixed_code.startswith("```"):
            lines = fixed_code.split("\n")
            fixed_code = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

        with open(filepath, "w") as f:
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