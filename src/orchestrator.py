from src.utils.logger import log_experiment, ActionType
from src.agents.auditeur import AuditorAgent
from src.agents.correcteur import FixerAgent
from src.agents.debugueur import TesterAgent


class Orchestrator:

    def __init__(self, target_dir, max_iterations=4):

        self.target_dir = target_dir
        self.max_iterations = max_iterations

        #  Initialize agents
        self.auditor = AuditorAgent()
        self.fixer = FixerAgent()
        self.tester = TesterAgent()

    def run(self):

        print(" Running Auditor...")

        audit_report = self.auditor.analyze(self.target_dir)

        print(" Audit Report:", audit_report)

        for iteration in range(self.max_iterations):

            print(f"\n ITERATION {iteration + 1}")

            #  Test all files
            test_result = self.tester.test(self.target_dir)

            print(" TEST RESULT =", test_result)

            #  Check if everything passed
            all_passed = all(
                result["passed"]
                for result in test_result.values()
            )

            if all_passed:

                print(" ALL TESTS PASSED")

                return {
                    "success": True,
                    "iterations": iteration + 1
                }

            #  Fix failed files
            for filename, result in test_result.items():

                if not result["passed"]:

                    print(f"Fixing {filename}")

                    self.fixer.fix(
                        self.target_dir,
                        filename,
                        result["output"]
                    )

        print(" MAX ITERATIONS REACHED")

        return {
            "success": False,
            "iterations": self.max_iterations
        }