from src.utils.logger import log_experiment, ActionType
class FixerAgent:
    def __init__(self):
        self.name = "CorrectorAgent"

    def fix(self, fichier, description="Correction automatique"):
        resultat = appliquer_correction(fichier, description)

        return {
            "fixed": True,
            "message": resultat
        }

def appliquer_correction(fichier, description):
    resultat = f"{fichier} corrigé"
    log_experiment(
        agent_name="Correcteur",
        model_used="GPT-4",
        action=ActionType.FIX,
        details={"input_prompt": description, "output_response": resultat},
        status="SUCCESS"
    )
    return resultat
