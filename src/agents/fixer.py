class FixerAgent:
    def fix(self, target_dir, issues):
        for issue in issues:
            file = issue.get("file", "unknown")
            print(f"Fix requested for {file}")
