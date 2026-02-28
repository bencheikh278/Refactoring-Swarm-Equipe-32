from openai import OpenAI
import os
from src.utils.file_tools import read_file, write_file


class FixerAgent:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        #  PROMPT INSIDE AGENT
        self.system_prompt = """
You are a Python fixer.
You receive code + errors.
Return ONLY corrected full file code.
Do not add explanations.
"""

    def fix(self, target_dir, filename, error_output):

        code = read_file(filename)

        if not code:
            return False

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": f"""
File: {filename}

Code:
{code}

Errors:
{error_output}
"""
                }
            ]
        )

        fixed_code = response.choices[0].message.content

        write_file(filename, fixed_code)

        print(f" Fixed: {filename}")

        return True