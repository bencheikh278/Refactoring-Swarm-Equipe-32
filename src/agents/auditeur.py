from openai import OpenAI
import os
from src.utils.file_tools import read_file


class AuditorAgent:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # 🔥 PROMPT INSIDE AGENT
        self.system_prompt = """
You are a static code auditor.
Analyze Python code and return a JSON report with:
- problems
- file issues
- improvement suggestions
Return ONLY JSON.
"""

    def analyze(self, target_dir):

        import os
        reports = []

        for file in os.listdir(target_dir):

            if file.endswith(".py"):

                code = read_file(file)

                if not code:
                    continue

                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": code}
                    ]
                )

                report = response.choices[0].message.content

                reports.append({
                    "file": file,
                    "report": report
                })

        return reports