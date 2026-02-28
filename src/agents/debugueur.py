from src.utils.logger import log_experiment, ActionType
from src.utils.Corrector import run_pytest_for_file
import os


class TesterAgent:

    def __init__(self):
        self.name = "DebuggerAgent"

    def test(self, target_dir):

        results = {}

        for file in os.listdir(target_dir):
            if file.endswith(".py"):


                result = run_pytest_for_file(file)

                results[file] = result

                # ✅ Log inside loop (so filename exists)
                status = "SUCCESS" if result.get("passed") else "FAILURE"

                log_experiment(
                    agent_name="Débogueur",
                    model_used="local",
                    action=ActionType.DEBUG,
                    details={
                        "input_prompt": f"Tests {file}",
                        "output_response": result.get("output")
                    },
                    status=status
                )

        return results