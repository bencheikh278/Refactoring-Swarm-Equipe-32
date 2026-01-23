import json
import os
import uuid
from datetime import datetime
from enum import Enum

LOG_FILE = os.path.join("logs", "experiment_data.json")

class ActionType(str, Enum):
    ANALYSIS = "CODE_ANALYSIS"
    GENERATION = "CODE_GEN"
    DEBUG = "DEBUG"
    FIX = "FIX"

def log_experiment(agent_name: str, model_used: str, action: ActionType, details: dict, status: str):
    if isinstance(action, ActionType):
        action_str = action.value
    else:
        raise ValueError(f"Action invalide : {action}")

    if action_str in [ActionType.ANALYSIS.value, ActionType.GENERATION.value,
                      ActionType.DEBUG.value, ActionType.FIX.value]:
        required_keys = ["input_prompt", "output_response"]
        missing_keys = [k for k in required_keys if k not in details]
        if missing_keys:
            raise ValueError(f"Champs manquants dans details: {missing_keys}")

    os.makedirs("logs", exist_ok=True)

    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "model": model_used,
        "action": action_str,
        "details": details,
        "status": status
    }

    data = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
        except json.JSONDecodeError:
            print(f"⚠️ Fichier {LOG_FILE} corrompu, création d'une nouvelle liste")
            data = []

    data.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
