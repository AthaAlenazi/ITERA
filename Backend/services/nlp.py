import json
import os

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, "knowledge_base.json")


# Load AI model
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_knowledge_base():

    with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


# Load knowledge base once
knowledge_base = load_knowledge_base()


# Prepare keyword embeddings once
category_embeddings = {}

for problem_type, data in knowledge_base.items():

    keywords = data["keywords"]

    category_embeddings[problem_type] = {
        "keywords": keywords,
        "embeddings": model.encode(keywords)
    }


def semantic_diagnosis(problem: str):

    problem = problem.strip()

    if not problem:
        return {
            "problem_type": None,
            "score": 0.0
        }

    problem_embedding = model.encode([problem])

    best_problem_type = None
    best_score = 0.0

    for problem_type, data in category_embeddings.items():

        scores = cosine_similarity(
            problem_embedding,
            data["embeddings"]
        )[0]

        category_score = float(max(scores))

        if category_score > best_score:

            best_score = category_score
            best_problem_type = problem_type

    return {
        "problem_type": best_problem_type,
        "score": best_score
    }