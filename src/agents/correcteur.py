from openai import OpenAI
import os


class FixerAgent:

    def __init__(self):

        # Load API client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Load system prompt safely
        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        prompt_path = os.path.join(
         base_dir,
         "prompts",
          "correcteur_prompts.md"
           )

        with open(prompt_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def fix(self, target_dir, filename, error_output):

        filepath = os.path.join(target_dir, filename)

        # Read file content
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()

        #  Call AI model
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": f"""
Code:
{code}

Errors:
{error_output}

Return ONLY corrected code.
"""
                }
            ]
        )

        fixed_code = response.choices[0].message.content

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(fixed_code)

        return True