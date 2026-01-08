import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.logger import log_experiment, ActionType


agents = ["Auditeur", "Correcteur", "Débogueur", "Générateur de tests"]
actions = [ActionType.ANALYSIS, ActionType.FIX, ActionType.DEBUG, ActionType.GENERATION]

for agent, action in zip(agents, actions):
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

print(" Tous les types d'actions ont été loggés avec succès !")
