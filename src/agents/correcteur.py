from src.utils.file_tools import simple_corrector
from src.utils.logger import log_experiment, ActionType
import os


class FixerAgent:
    def __init__(self):
        self.name = "FixerAgent"

    def fix(self, target_dir, filename, issues=None):

        filepath = os.path.join(target_dir, filename)

        success = simple_corrector(filepath)

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