import argparse
import sys
import os
from dotenv import load_dotenv
from src.utils.logger import log_experiment, ActionType

load_dotenv()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", type=str, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.target_dir):
        print(f"❌ Dossier {args.target_dir} introuvable.")
        sys.exit(1)

    print(f"🚀 DEMARRAGE SUR : {args.target_dir}")

    # --- TEST LOGGER (Data Officer) ---
    log_experiment(
        agent_name="System",
        model_used="N/A",
        action=ActionType.ANALYSIS,
        details={"input_prompt": "Initialisation TP", "output_response": "Logger OK"},
        status="SUCCESS"
    )
    print("✅ Logger testé avec succès")

    # Ici viendrait le reste de l'orchestration des agents
    print("✅ MISSION_COMPLETE")

if __name__ == "__main__":
    main()
