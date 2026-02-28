from src.utils.logger import log_experiment, ActionType
from src.utils.Corrector import run_pytest_for_file
import os


class TesterAgent:

    def __init__(self):
        self.name = "TesterAgent"

    def test(self, target_dir):
        """Exécute les tests pytest sur chaque fichier Python du dossier."""

        results = {}

        for file in os.listdir(target_dir):
            if file.endswith(".py"):

                # On passe uniquement le nom du fichier (pas le chemin complet)
                result = run_pytest_for_file(file)

                results[file] = result

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