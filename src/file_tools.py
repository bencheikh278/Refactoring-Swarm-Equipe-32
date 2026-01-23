import os
from utils.logger import log_experiment, ActionType  # Pour loguer les actions

# Chemin du sandbox
SANDBOX_DIR = os.path.join(os.path.dirname(__file__), '..', 'sandbox')
os.makedirs(SANDBOX_DIR, exist_ok=True)  # Crée le dossier s'il n'existe pas

def write_file(filename, content):
    """
    Écrit du texte dans un fichier dans /sandbox et logue l'action
    """
    filepath = os.path.join(SANDBOX_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Log de l'action
    log_experiment(
        agent_name="Tool",
        model_used="local",
        action=ActionType.GENERATION,
        details={"input_prompt": "N/A", "output_response": content},
        status="SUCCESS"
    )

    print(f"Fichier écrit : {filepath}")


def read_file(filename):
    """
    Lit le contenu d'un fichier dans /sandbox et logue l'action
    """
    filepath = os.path.join(SANDBOX_DIR, filename)
    
    if not os.path.exists(filepath):
        # Log d'erreur si fichier introuvable
        log_experiment(
            agent_name="Tool",
            model_used="local",
            action=ActionType.DEBUG,
            details={"input_prompt": "N/A", "output_response": ""},
            status="FAILURE"
        )
        print(f"Fichier introuvable : {filepath}")
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Log de lecture réussie
    log_experiment(
        agent_name="Tool",
        model_used="local",
        action=ActionType.ANALYSIS,
        details={"input_prompt": "N/A", "output_response": content},
        status="SUCCESS"
    )

    print(f"Fichier lu : {filepath}")
    return content
