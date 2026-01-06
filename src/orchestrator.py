
from src.utils.logger import log_experiment, ActionType
from src.agents.auditor import AuditorAgent
from src.agents.fixer import FixerAgent
from src.agents.tester import TesterAgent

class Orchestrator:
    def __init__(self, target_dir, max_iterations=15):
        self.target_dir = target_dir
        self.max_iterations = max_iterations
#initialisation des agents
        self.auditor = AuditorAgent()
        self.fixer = FixerAgent()
        self.tester = TesterAgent()

    def run(self):
        #analyse phase

        issues = self.auditor.analyze(self.target_dir)
#phase2 and 3: fixing and testing

        for iteration in range(self.max_iterations):
            #fix
            self.fixer.fix(self.target_dir, issues)
#test
            test_result = self.tester.test(self.target_dir)

            if test_result["passed"]:
                return {
                    "success": True,
                    "iterations": iteration + 1
                }

            issues = test_result["errors"]

        return {
            "success": False,
            "iterations": self.max_iterations
        }
