import json
import os

sandbox_dir = "sandbox"
logs_file = os.path.join(sandbox_dir, "logs/experiment_data.json")

with open(logs_file) as f:
    logs = json.load(f)

for entry in logs:
    if entry["action"] == "FIX" and entry["status"] == "SUCCESS":
        details = entry["details"]
        # Cherche le fichier parmi les fichiers existants
        fichier_trouve = None
        for f in os.listdir(sandbox_dir):
            if f.endswith(".py") and f in details.get("input_prompt", ""):
                fichier_trouve = f
                break

        if fichier_trouve:
            contenu_path = os.path.join(sandbox_dir, fichier_trouve)
            corrige_path = os.path.join(sandbox_dir, fichier_trouve.replace(".py", "_corrige.py"))

            with open(contenu_path) as cf:
                code = cf.read()

            # Ici on simule la correction
            code_corrige = code + f"\n# Correction appliquée : {details.get('output_response', '')}"

            with open(corrige_path, "w") as cf:
                cf.write(code_corrige)

            print(f"{fichier_trouve} -> correction appliquée : {corrige_path}")
        else:
            print(f"{details.get('input_prompt', '')} -> aucune correction trouvée")
