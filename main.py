import argparse
import sys
import os
from groq import Groq
from dotenv import load_dotenv
from src.utils.logger import log_experiment, ActionType
from src.orchestrator import Orchestrator

load_dotenv()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", type=str, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.target_dir):
        print(f"❌ Dossier {args.target_dir} introuvable.")
        sys.exit(1)

    print(f"🚀 DEMARRAGE SUR : {args.target_dir}")

    # --- Initialisation Groq ---
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY manquante dans le fichier .env")
        sys.exit(1)

    client = Groq(api_key=api_key)

    # --- TEST LOGGER ---
    log_experiment(
        agent_name="System",
        model_used="N/A",
        action=ActionType.ANALYSIS,
        details={"input_prompt": "Initialisation", "output_response": "Logger OK"},
        status="SUCCESS"
    )
    print("✅ Logger testé avec succès")

    # --- Lancement de l'orchestrateur ---
    try:
        orchestrator = Orchestrator(args.target_dir, client=client)
        result = orchestrator.run()

        if result.get("success"):
            print("🎯 MISSION_COMPLETE")
            sys.exit(0)
        else:
            print("❌ MISSION_FAILED")
            print("Details:", result)
            sys.exit(1)

    except Exception as e:
        print(f"ERREUR : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()