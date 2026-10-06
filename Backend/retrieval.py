import json
import os

from services.nlp import model


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, "knowledge_base.json")


def load_knowledge_base():

    with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def retrieve_knowledge(problem: str):

    if not problem or not problem.strip():

        return []

    knowledge_base = load_knowledge_base()

    problem_embedding = model.encode([problem])

    results = []

    from sklearn.metrics.pairwise import cosine_similarity

    for problem_type, data in knowledge_base.items():

        keywords = data["keywords"]

        keyword_embeddings = model.encode(keywords)

        scores = cosine_similarity(
            problem_embedding,
            keyword_embeddings
        )[0]

        score = float(max(scores))

        results.append({
            "problem_type": problem_type,
            "category": data["category"],
            "diagnosis": data["diagnosis"],
            "score": score,
            "solution": data["solution"]
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:3]