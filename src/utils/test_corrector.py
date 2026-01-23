# test_corrector.py
from Corrector import simple_corrector, run_pytest_on_sandbox

# 1️⃣ Corriger un fichier spécifique
simple_corrector("test_test.py")  # ton fichier modifié dans sandbox

# 2️⃣ Tester tous les fichiers du sandbox et récupérer les résultats
results = run_pytest_on_sandbox()

# 3️⃣ Afficher les résultats
for r in results:
    print(f"Fichier : {r['file']}, Passed : {r['passed']}")
    print(f"Output :\n{r['output']}\n")
