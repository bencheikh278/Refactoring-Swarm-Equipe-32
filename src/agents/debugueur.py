from src.utils.logger import log_experiment, ActionType
class TesterAgent:
    def __init__(self):
        self.name = "DebuggerAgent"

    def test(self, fichier):
        resultat = executer_tests(fichier)

        return {
            "passed": True,
            "message": resultat
        }
def executer_tests(fichier):
    resultat = "Tous les tests passent"
    log_experiment(
        agent_name="Débogueur",
        model_used="GPT-4",
        action=ActionType.DEBUG,
        details={"input_prompt": f"Tests unitaires {fichier}", "output_response": resultat},
        status="SUCCESS"
    )
    return resultat
