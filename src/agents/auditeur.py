from src.utils.logger import log_experiment, ActionType
from src.utils.file_tools import read_file_and_check_syntax  # adjust import if needed

class AuditorAgent:
    def __init__(self):
        self.name = "AuditorAgent"

    def analyze(self, filename):

        content, error = read_file_and_check_syntax(filename)

        if error:
            status = "FAILURE"
            message = error
            issues = 1
        else:
            status = "SUCCESS"
            message = f"Aucune erreur détectée dans {filename}"
            issues = 0

        log_experiment(
            agent_name="Auditeur",
            model_used="local",
            action=ActionType.ANALYSIS,
            details={
                "input_prompt": f"Analyse {filename}",
                "output_response": message
            },
            status=status
        )

        return {
            "issues_found": issues,
            "message": message
        }
