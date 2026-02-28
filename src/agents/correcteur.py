from src.utils.logger import log_experiment, ActionType
from src.utils.Corrector import simple_corrector

class FixerAgent:
    def __init__(self):
        self.name = "CorrectorAgent"

def fix(self, target_dir, issues):

        success = simple_corrector(target_dir)

        status = "SUCCESS" if success else "FAILURE"

        log_experiment(
            agent_name="Correcteur",
            model_used="local",
            action=ActionType.FIX,
            details={
                "input_prompt": f"Correction {filename}",
                "output_response": "Correction appliquée"
            },
            status=status
        )

        return success
