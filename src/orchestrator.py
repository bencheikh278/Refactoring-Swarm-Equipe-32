# src/orchestrator.py

from src.agents import auditeur, correcteur, debugueur, generateur_tests
from src.utils.logger import log_experiment, ActionType

class Orchestrator:
    def __init__(self, target_dir):
        self.target_dir = target_dir

    def run(self):
        try:
            # 1. Analyse main.py
            auditeur.analyser_fichier("main.py")

            # 2. Correction main.py
            correcteur.appliquer_correction("main.py", "Correction docstrings et indentation")

            # 3. Débogage main.py
            debugueur.executer_tests("main.py")

            # 4. Génération de tests main.py
            generateur_tests.creer_tests("main.py")

            # 5. Analyse utils.py avec erreur simulée
            auditeur.analyser_fichier("utils.py", resultat="1 erreur détectée", status="FAILURE")

            # 6. Correction utils.py
            correcteur.appliquer_correction("utils.py", "Correction de l'erreur utils.py")

            # 7. Tests génériques pour validation
            for fichier in ["test_code_analysis", "test_fix", "test_debug", "test_code_gen"]:
                auditeur.analyser_fichier(fichier)
                correcteur.appliquer_correction(fichier, "Test FIX")
                debugueur.executer_tests(fichier)
                generateur_tests.creer_tests(fichier)

            return {"success": True, "message": "TP exécuté avec succès"}
        except Exception as e:
            return {"success": False, "message": str(e)}
