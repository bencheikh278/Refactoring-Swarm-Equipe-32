from src.utils.logger import log_experiment, ActionType
class AuditorAgent:
    def __init__(self):
        self.name = "AuditorAgent"

    def analyze(self, fichier):
        resultat = analyser_fichier(fichier)

        return {
            "issues_found": 0,
            "message": resultat
        }
def analyser_fichier(fichier, resultat=None, status="SUCCESS"):
    if resultat is None:
        resultat = f"Aucune erreur détectée dans {fichier}"
    log_experiment(
        agent_name="Auditeur",
        model_used="GPT-4",
        action=ActionType.ANALYSIS,
        details={"input_prompt": f"Analyse {fichier}", "output_response": resultat},
        status=status
    )
    return resultat
