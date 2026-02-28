import os
from src.utils.logger import log_experiment, ActionType
from src.agents.auditeur import AuditorAgent
from src.agents.correcteur import FixerAgent
from src.agents.debugueur import TesterAgent


class Orchestrator:
    def __init__(self, target_dir, client, max_iterations=10):
        self.target_dir = target_dir
        self.max_iterations = max_iterations

        self.auditor = AuditorAgent(client=client)
        self.fixer = FixerAgent(client=client)
        self.tester = TesterAgent()

    def run(self):

        print("🔍 Analyse du code en cours...")
        issues = self.auditor.analyze(self.target_dir)

        for iteration in range(self.max_iterations):
            print(f"\n🔄 Itération {iteration + 1}/{self.max_iterations}")

            if isinstance(issues, list):
                for issue in issues:
                    filename = issue["file"] if isinstance(issue, dict) else issue
                    self.fixer.fix(self.target_dir, filename, issues=issue)
            else:
                for file in os.listdir(self.target_dir):
                    if file.endswith(".py"):
                        self.fixer.fix(self.target_dir, file, issues=issues)

            test_result = self.tester.test(self.target_dir)
            print("TEST RESULT =", test_result)

            all_passed = all(
                file_result.get("passed", False)
                or "no tests ran" in file_result.get("output", "")
                for file_result in test_result.values()
            )

            if all_passed:
                print("🎯 ALL TESTS PASSED")
                return {"success": True, "iterations": iteration + 1}

            issues = [
                {"file": fname, "errors": res.get("output", "")}
                for fname, res in test_result.items()
                if not res.get("passed", False)
                and "no tests ran" not in res.get("output", "")
            ]

            if not issues:
                print("🎯 CODE CORRIGE - Aucune erreur restante")
                return {"success": True, "iterations": iteration + 1}

        return {
            "success": False,
            "iterations": self.max_iterations
        }