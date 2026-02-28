import os
from openai import OpenAI
from src.utils.Corrector import run_pytest_for_file


class TesterAgent:

    def __init__(self):
        self.name = "TesterAgent"

    def test(self, target_dir):
        """Exécute les tests pytest sur chaque fichier Python du dossier."""

        results = {}

        for file in os.listdir(target_dir):

                # On passe uniquement le nom du fichier (pas le chemin complet)
                result = run_pytest_for_file(file)

                ai_evaluation = response.choices[0].message.content

                status = "SUCCESS" if result.get("passed") else "FAILURE"

                log_experiment(
                    agent_name="Testeur",
                    model_used="local",
                    action=ActionType.DEBUG,
                    details={
                        "input_prompt": f"Tests {file}",
                        "output_response": result.get("output", "")
                    },
                    status=status
                )

        return results