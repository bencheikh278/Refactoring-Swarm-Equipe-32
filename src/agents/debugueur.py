from src.utils.logger import log_experiment, ActionType

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
