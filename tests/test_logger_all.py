import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.logger import log_experiment, ActionType

class TestLoggerAll(unittest.TestCase):

    def test_all_actions(self):
        """Teste que toutes les actions peuvent être loggées sans erreur"""
        agents = ["Auditeur", "Correcteur", "Débogueur", "Générateur de tests"]
        actions = [ActionType.ANALYSIS, ActionType.FIX, ActionType.DEBUG, ActionType.GENERATION]

        for agent, action in zip(agents, actions):
            try:
                log_experiment(
                    agent_name=agent,
                    model_used="GPT-4",
                    action=action,
                    details={
                        "input_prompt": f"Test {action.value}",
                        "output_response": "OK"
                    },
                    status="SUCCESS"
                )
            except Exception as e:
                self.fail(f"log_experiment a échoué pour {agent} / {action}: {e}")

if __name__ == "__main__":
    unittest.main()
