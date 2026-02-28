import os
import subprocess
from src.utils.logger import log_experiment, ActionType


# Chemin vers sandbox depuis utils
SANDBOX_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'sandbox'))
print("SANDBOX_DIR =", SANDBOX_DIR)

# -----------------------------
# Correcteur sécurisé
# -----------------------------
def simple_corrector(filename):
    """
    Corrige les erreurs simples d'un fichier Python :
    - Ajoute des docstrings si manquantes pour chaque fonction
    - Corrige l'indentation simple
    - Logue chaque correction
    Sécurité : ne peut modifier que les fichiers dans sandbox
    """
    filepath = os.path.abspath(os.path.join(SANDBOX_DIR, filename))
    if not filepath.startswith(os.path.abspath(SANDBOX_DIR) + os.sep):
        print(f"❌ Interdiction d'écrire en dehors du sandbox : {filepath}")
        log_experiment(
            agent_name="Tool",
            model_used="local",
            action=ActionType.DEBUG,
            details={"input_prompt": "Correction simple", "output_response": f"Tentative d'accès non autorisé : {filepath}"},
            status="FAILURE"
        )
        return False

    if not os.path.exists(filepath):
        print(f"❌ Fichier introuvable : {filepath}")
        log_experiment(
            agent_name="Tool",
            model_used="local",
            action=ActionType.DEBUG,
            details={"input_prompt": "Correction simple", "output_response": ""},
            status="FAILURE"
        )
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    corrected_lines = []
    for line in lines:
        stripped_line = line.lstrip()

        if stripped_line.startswith("def") and '"""' not in stripped_line:
            func_name = stripped_line.split('(')[0].replace("def", "").strip()
            corrected_lines.append(line.rstrip() + "\n")
            corrected_lines.append(f"    \"\"\"Fonction {func_name} auto-doc\"\"\"\n")
            continue

        corrected_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(corrected_lines)

    log_experiment(
        agent_name="Tool",
        model_used="local",
        action=ActionType.FIX,
        details={"input_prompt": f"Correction simple du fichier {filename}", "output_response": "Docstring ajoutée si manquante"},
        status="SUCCESS"
    )

    print(f"✅ Correction simple effectuée : {filename}")
    return True


# -----------------------------
# Pytest sur un fichier sécurisé
# -----------------------------
def run_pytest_for_file(filename):
    filepath = os.path.abspath(os.path.join(SANDBOX_DIR, filename))
    if not filepath.startswith(os.path.abspath(SANDBOX_DIR) + os.sep):
        return {"file": filename, "passed": False, "output": "Accès non autorisé"}

    if not os.path.exists(filepath):
        return {"file": filename, "passed": False, "output": "Fichier introuvable"}

    result = subprocess.run(
        ["python", "-m", "pytest", filepath, "--tb=short", "-q"],
        capture_output=True,
        text=True
    )

    return {
        "file": filename,
        "passed": result.returncode == 0,
        "output": result.stdout.strip() + "\n" + result.stderr.strip()
    }


# -----------------------------
# Pytest sur tout le sandbox
# -----------------------------
def run_pytest_on_sandbox():
    results = []
    for file in os.listdir(SANDBOX_DIR):
        if file.endswith(".py"):
            result = run_pytest_for_file(file)
            results.append(result)

            log_experiment(
                agent_name="Tool",
                model_used="groq",
                action=ActionType.ANALYSIS,
                details={"input_prompt": "Pytest run", "output_response": result["output"]},
                status="SUCCESS" if result["passed"] else "FAILURE"
            )
    return results