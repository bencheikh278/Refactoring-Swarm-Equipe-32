from src.utils.logger import log_experiment, ActionType

# Liste des actions à simuler
actions = [
    ("Auditeur", ActionType.ANALYSIS, "Analyse du fichier main.py", "Aucune erreur détectée", "SUCCESS"),
    ("Correcteur", ActionType.FIX, "Correction docstrings et indentation", "Fichier corrigé", "SUCCESS"),
    ("Débogueur", ActionType.DEBUG, "Exécution tests unitaires", "Tous les tests passent", "SUCCESS"),
    ("Générateur de tests", ActionType.GENERATION, "Création de tests pour main.py", "3 tests générés", "SUCCESS"),
    ("Auditeur", ActionType.ANALYSIS, "Analyse du fichier utils.py", "1 erreur détectée", "FAILURE"),
    ("Correcteur", ActionType.FIX, "Correction de l'erreur utils.py", "Erreur corrigée", "SUCCESS"),
]

# Boucle pour remplir le JSON automatiquement
for agent_name, action_type, input_prompt, output_response, status in actions:
    log_experiment(
        agent_name=agent_name,
        model_used="GPT-4",
        action=action_type,
        details={
            "input_prompt": input_prompt,
            "output_response": output_response
        },
        status=status
    )

print(" JSON rempli avec succès ")
