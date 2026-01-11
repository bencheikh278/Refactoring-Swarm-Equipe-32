

# Documentation des Prompts - Refactoring Swarm

## 📊 Aperçu
Cette documentation décrit les 3 prompts système utilisés par les agents autonomes du système de refactoring.

## 🤖 Agent Auditeur
**Fichier** : `prompts/auditor_prompt.md`
**Responsable** : Prompt Engineer
**Dernière mise à jour** : 12 janvier 2025

### Objectif
Analyser statiquement le code Python buggé et produire un plan de refactoring détaillé.

### Format d'Entrée
- Dossier contenant des fichiers Python
- Aucune exécution de code

### Format de Sortie
JSON structuré avec :
- Liste des fichiers analysés
- Problèmes détectés par catégorie
- Plan de correction priorisé

### Exemple d'Usage
```python
# Dans main.py
with open('prompts/auditor_prompt.md', 'r') as f:
    system_prompt = f.read()
# Envoyer à LLM avec le code à analyser