"""
Point d'entrée du système Refactoring Swarm
"""
import argparse
import sys
import os
from dotenv import load_dotenv
from src.utils.logger import log_experiment, ActionType
from src.orchestrator import Orchestrator

load_dotenv()


def main():
    """
    Fonction principale du programme
    """
    parser = argparse.ArgumentParser(
        description="Système de refactoring automatique multi-agents"
    )
    parser.add_argument(
        "--target_dir",
        type=str,
        required=True,
        help="Chemin vers le dossier contenant le code à réparer"
    )
    args = parser.parse_args()

    if not os.path.exists(args.target_dir):
        print(f"❌ Dossier {args.target_dir} introuvable.")
        sys.exit(1)

    print(f"🚀 DEMARRAGE SUR : {args.target_dir}")
    
    log_experiment(
        agent_name="System",
        model_used="gemini-2.0-flash-exp",
        action=ActionType.ANALYSIS,
        details={
            "input_prompt": f"Target directory: {args.target_dir}",
            "output_response": "System initialized"
        },
        status="SUCCESS"
    )
    
    # Lance l'orchestrateur
    try:
        orchestrator = Orchestrator(args.target_dir)
        result = orchestrator.run()
        
        # Vérifie le résultat
        if result['success']:
            print(" MISSION_COMPLETE")
            sys.exit(0)
        else:
            print(f" MISSION_FAILED : {result['message']}")
            sys.exit(1)

   
        
    except Exception as e:
        print(f"ERREUR : {e}")
    
        sys.exit(1)


if __name__ == "__main__":
    main()