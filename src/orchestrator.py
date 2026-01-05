
from src.utils.logger import log_experiment, ActionType
from src.agents.auditor import AuditorAgent
from src.agents.fixer import FixerAgent
from src.agents.tester import TesterAgent

class Orchestrator:
    """
    Système multi-agents de refactoring
    """
    
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.max_iterations =15
        
        print(" Initialisation des agents")
        self.auditor = AuditorAgent()
        print(" Auditeur prêt")
        self.fixer = FixerAgent()
        print(" Correcteur prêt")
        self.tester = TesterAgent()
        print(" Testeur prêt")
    
    def run(self):
        """
        Lance le processus de refactoring
        """
        print("=" * 60)
        print("DÉBUT DU PROCESSUS")
        print("=" * 60)
        
        print("\n PHASE 1 : ANALYSE")
        issues = self.auditor.analyze(self.target_dir) #need this methode here
        print(f" {len(issues)} problem found")
        
        # Log de l'analyse
        log_experiment(
            agent_name="Auditor",
            model_used="gemini-2.0-flash-exp",
            action=ActionType.ANALYSIS,
            details={
                "input_prompt": f"Analyser le code dans {self.target_dir}",
                "output_response": f"Trouvé {len(issues)} problèmes"
            },
            status="SUCCESS"
        )
        #=============================================================================
        print("\n PHASE 2 : BOUCLE DE CORRECTION")

          
          
        #=============================================================================

        print("\n PHASE 3 : Tests...")
        
        
        return {
             'success': False,
            'iterations': self.max_iterations,
            'message': 'echc apres 15 tentatives'
        }