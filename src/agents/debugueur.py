from src.utils.logger import log_experiment, ActionType
from src.utils.Corrector import run_pytest_for_file

class TesterAgent:
    def __init__(self):
        self.name = "DebuggerAgent"

    def test(self, filename):

        filepath = os.path.join(target_dir, filename)
        result = run_pytest_for_file(filepath)

        status = "SUCCESS" if result["passed"] else "FAILURE"

        log_experiment(
            agent_name="Débogueur",
            model_used="local",
            action=ActionType.DEBUG,
            details={
                "input_prompt": f"Tests {filename}",
                "output_response": result["output"]
            },
            status=status
        )

        return result
