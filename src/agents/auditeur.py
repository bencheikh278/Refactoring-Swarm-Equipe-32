from src.utils.logger import log_experiment, ActionType
from src.utils.file_tools import read_file_and_check_syntax
import os


class AuditorAgent:
    def __init__(self):
        self.name = "AuditorAgent"

    def analyze(self, target_dir):
        """
        Analyse le code et retourne une liste des problèmes trouvés
        """
        issues_list = []

        for file in os.listdir(target_dir):
            if file.endswith(".py"):
                filepath = os.path.join(target_dir, file)
                content, error = read_file_and_check_syntax(filepath)

                if error:
                    issues_list.append(error)
                    status = "FAILURE"
                    message = error
                else:
                    status = "SUCCESS"
                    message = f"Aucune erreur détectée dans {file}"

                log_experiment(
                    agent_name="Auditeur",
                    model_used="local",
                    action=ActionType.ANALYSIS,
                    details={
                        "input_prompt": f"Analyse {file}",
                        "output_response": message
                    },
                    status=status
                )

        return issues_list
        
