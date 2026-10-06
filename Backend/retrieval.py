import json
import os

from services.nlp import calculate_similarity


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, "knowledge_base.json")


def load_knowledge_base():
    with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def retrieve_knowledge(problem: str):

    if not problem or not problem.strip():
        return []

    knowledge_base = load_knowledge_base()

    results = []

    for problem_type, data in knowledge_base.items():

        best_score = 0.0

        for keyword in data["keywords"]:

            score = calculate_similarity(
                problem,
                keyword
            )

            if score > best_score:
                best_score = score

        results.append({
            "problem_type": problem_type,
            "category": data["category"],
            "diagnosis": data["diagnosis"],
            "score": round(best_score, 4),
            "solution": data["solution"]
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:3]