import os
from src.utils.Corrector import run_pytest_for_file
from src.utils.logger import log_experiment, ActionType


class TesterAgent:

    def __init__(self):
        self.name = "TesterAgent"

    def test(self, target_dir):

        results = {}

        for file in os.listdir(target_dir):

            if file.endswith(".py"):

                result = run_pytest_for_file(file)

                results[file] = result

                log_experiment(
                    agent_name="Testeur",
                    model_used="local",
                    action=ActionType.DEBUG,
                    details={
                        "input_prompt": f"Tests {file}",
                        "output_response": result.get("output", "")
                    },
                    status="SUCCESS" if result.get("passed") else "FAILURE"
                )

        return results