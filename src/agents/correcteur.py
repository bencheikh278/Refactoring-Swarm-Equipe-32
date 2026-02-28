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

        # Lire avec UTF-8
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()

        with open("prompts/correcteur_prompts.md", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        full_prompt = f"""
{system_prompt}

Plan de correction :
{issues}

Code a corriger ({filename}) :
{code}

Retourne uniquement le code Python corrige complet, sans balises markdown.
Le fichier doit commencer par: # -*- coding: utf-8 -*-
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": full_prompt}]
        )

        fixed_code = response.choices[0].message.content

        # Nettoyer les balises markdown si presentes
        if fixed_code.startswith("```"):
            lines = fixed_code.split("\n")
            fixed_code = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

        # Ajouter l'encodage si absent
        if "coding: utf-8" not in fixed_code[:50]:
            fixed_code = "# -*- coding: utf-8 -*-\n" + fixed_code

        # Ecrire avec UTF-8
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