from src.utils.logger import log_experiment, ActionType
from src.utils.Corrector import run_pytest_for_file

class TesterAgent:
    def __init__(self):
        self.name = "DebuggerAgent"

    def test(self, target_dir):

        result = run_pytest_for_file(target_dir)

        status = "SUCCESS" if result["passed"] else "FAILURE"

        log_experiment(
            agent_name="Débogueur",
            model_used="local",
            action=ActionType.DEBUG,
            details={
                "input_prompt": f"Tests {target_dir}",
                "output_response": result["output"]
            },
            status=status
        )

        return result
