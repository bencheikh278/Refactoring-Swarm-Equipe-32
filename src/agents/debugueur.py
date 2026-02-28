import os
from openai import OpenAI
from src.utils.Corrector import run_pytest_for_file


class TesterAgent:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # 🔥 PROMPT IS USED NOW
        self.system_prompt = """
You analyze pytest output.
Return:
- passed (true/false)
- summary
- recommendations
Return JSON only.
"""

    def test(self, target_dir):

        results = {}

        for file in os.listdir(target_dir):

            if file.endswith(".py"):

                pytest_result = run_pytest_for_file(file)

                # Send pytest output to AI
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {
                            "role": "user",
                            "content": pytest_result["output"]
                        }
                    ]
                )

                ai_evaluation = response.choices[0].message.content

                results[file] = {
                    "pytest": pytest_result,
                    "ai_evaluation": ai_evaluation
                }

                print(f" AI Tested {file}")

        return results