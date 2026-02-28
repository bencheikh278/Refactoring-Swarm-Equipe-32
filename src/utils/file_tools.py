import os
from src.utils.logger import log_experiment, ActionType  # ton logger existant
from src.utils.Corrector import simple_corrector
# -----------------------------
# Chemin vers le sandbox
# -----------------------------
SANDBOX_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'sandbox'))
print("SANDBOX_DIR =", SANDBOX_DIR)
# -----------------------------
# Écriture sécurisée dans sandbox
# -----------------------------
def write_file(filename, content):
    """
    Écrit du texte dans un fichier du sandbox et logue l'action.
    """
    # Vérification sécurité : n'autoriser que sandbox
    # If filename is already absolute → use it
    if os.path.isabs(filename):
     filepath = filename
    else:
     filepath = os.path.join(SANDBOX_DIR, os.path.basename(filename))

    filepath = os.path.abspath(filepath)
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

    print(f"✅ Fichier écrit : {filepath}")
    return filepath

# -----------------------------
# Lecture sécurisée depuis sandbox
# -----------------------------
def read_file(filename):
    """
    Lit le contenu d'un fichier du sandbox et logue l'action.
    """
    if not os.path.exists(SANDBOX_DIR):
        raise FileNotFoundError(f"Le dossier sandbox n'existe pas : {SANDBOX_DIR}")
    filepath = os.path.join(SANDBOX_DIR, os.path.basename(filename))

    if not os.path.exists(filepath):
        log_experiment(
            agent_name="Tool",
            model_used="local",
            action=ActionType.DEBUG,
            details={"input_prompt": "N/A", "output_response": ""},
            status="FAILURE"
        )
        print(f"❌ Fichier introuvable : {filepath}")
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    log_experiment(
        agent_name="Tool",
        model_used="local",
        action=ActionType.ANALYSIS,
        details={"input_prompt": "N/A", "output_response": content},
        status="SUCCESS"
    )

    print(f"📖 Fichier lu : {filepath}")
    return content

# -----------------------------
# Lecture + détection des erreurs de syntaxe
# -----------------------------
def read_file_and_check_syntax(filename):
    """
    Lit un fichier dans le sandbox et détecte les erreurs de syntaxe.
    Retourne un tuple : (contenu, erreur_syntaxe)
    """
    content = read_file(filename)
    if content is None:
        return None, "Fichier introuvable"

    try:
        compile(content, filename, "exec")  # teste la syntaxe sans exécuter
        return content, None  # pas d'erreur
    except SyntaxError as e:
        return content, f"Erreur de syntaxe ligne {e.lineno}: {e.msg}"

# -----------------------------
# Exemple de test rapide
# -----------------------------
if __name__ == "__main__":
    # Écriture test
    write_file("test_example.py", "def add(a, b):\n    return a + b\n")

    # Lecture et détection syntaxe
    content, error = read_file_and_check_syntax("test_example.py")
    if error:
        print("❌", error)
    else:
        print("✅ Syntaxe correcte !")
