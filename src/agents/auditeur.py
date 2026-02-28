from src.utils.logger import log_experiment, ActionType
from src.utils.file_tools import read_file_and_check_syntax


class AuditorAgent:
    def __init__(self):
        self.name = "AuditorAgent"

    def analyze(self, target_dir):
        """
        Analyse le code et retourne une liste de problèmes
        
        Returns:
            list: Liste des problèmes trouvés
        """
        content, error = read_file_and_check_syntax(target_dir)

        if error:
            status = "FAILURE"
            message = error
            issues_list = [error]  
        else:
            status = "SUCCESS"
            message = f"Aucune erreur détectée dans {target_dir}"
            issues_list = []  

        log_experiment(
            agent_name="Auditeur",
            model_used="local",
            action=ActionType.ANALYSIS,
            details={
                "input_prompt": f"Analyse {target_dir}",
                "output_response": message
            },
            status=status
        )


        return issues_list
