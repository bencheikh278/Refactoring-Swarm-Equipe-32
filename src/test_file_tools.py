from file_tools import write_file, read_file

# 1️⃣ Écriture d'un fichier de test
write_file("test.txt", "Bonjour, ceci est un test TP IGL !")

# 2️⃣ Lecture du fichier de test
content = read_file("test.txt")
print("Contenu lu :", content)

# 3️⃣ Test d'un fichier inexistant
content_none = read_file("fichier_inexistant.txt")
print("Lecture fichier inexistant :", content_none)
