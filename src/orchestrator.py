import os
from src.agents.auditeur import AuditorAgent
from src.agents.correcteur import FixerAgent
from src.agents.debugueur import TesterAgent


class Orchestrator:

    def __init__(self, target_dir, client, max_iterations=3):

        self.target_dir = target_dir
        self.max_iterations = max_iterations

        self.auditor = AuditorAgent(client)
        self.fixer = FixerAgent(client)
        self.tester = TesterAgent()

    def run(self):

        print("🔍 Running Auditor...")
        issues = self.auditor.analyze(self.target_dir)

        for iteration in range(self.max_iterations):

            print(f"\n🔄 Iteration {iteration+1}")

            # Fix phase
            for file in os.listdir(self.target_dir):
                if file.endswith(".py"):
                    self.fixer.fix(
                        self.target_dir,
                        file,
                        issues
                    )

            # Test phase
            test_result = self.tester.test(self.target_dir)

            print("TEST RESULT =", test_result)

            if all(res["passed"] for res in test_result.values()):
                print("🎯 ALL TESTS PASSED")
                return {
                    "success": True,
                    "iterations": iteration + 1
                }

            print("❌ Tests failed → Refactoring again")

        return {
            "success": False,
            "iterations": self.max_iterations
        }