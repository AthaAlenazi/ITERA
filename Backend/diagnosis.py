import json
import os

from services.nlp import semantic_diagnosis


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, "knowledge_base.json")


def load_knowledge_base():
    with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def diagnose_problem(problem: str):

    if not problem or not problem.strip():
        return {
            "diagnosis": "No problem description provided",
            "category": "Other",
            "confidence": 0,
            "solution": [
                "Please describe your IT problem.",
                "You can also upload a screenshot to help ITERA analyze the issue."
            ],
            "it_required": False
        }

    knowledge_base = load_knowledge_base()

    nlp_result = semantic_diagnosis(problem)

    problem_type = nlp_result.get("problem_type")
    score = nlp_result.get("score", 0)

    confidence = round(score * 100)

    if not problem_type or problem_type not in knowledge_base or score < 0.35:

        return {
            "diagnosis": "Unknown IT problem",
            "category": "Other",
            "confidence": confidence,
            "solution": [
                "Please provide more details about the problem.",
                "You can also upload a screenshot to help ITERA analyze the issue.",
                "If the problem requires IT intervention, contact IT support."
            ],
            "it_required": True
        }

    data = knowledge_base[problem_type]

    return {
        "diagnosis": data["diagnosis"],
        "category": data["category"],
        "confidence": confidence,
        "solution": data["solution"],
        "it_required": data["it_required"]
    }