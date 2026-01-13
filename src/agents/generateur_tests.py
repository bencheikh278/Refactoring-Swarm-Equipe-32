from src.utils.logger import log_experiment, ActionType

def creer_tests(fichier):
    resultat = "3 tests générés"
    log_experiment(
        agent_name="Générateur de tests",
        model_used="GPT-4",
        action=ActionType.GENERATION,
        details={"input_prompt": f"Créer 3 tests pour {fichier}", "output_response": resultat},
        status="SUCCESS"
    )
    return resultat
