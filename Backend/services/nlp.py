import json
import os
import re
from difflib import SequenceMatcher

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, "knowledge_base.json")


def load_knowledge_base():
    with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


knowledge_base = load_knowledge_base()


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def calculate_similarity(problem, keyword):
    problem = normalize_text(problem)
    keyword = normalize_text(keyword)

    if not problem or not keyword:
        return 0.0

    # Exact phrase match
    if keyword in problem:
        return 1.0

    problem_words = set(problem.split())
    keyword_words = set(keyword.split())

    if not keyword_words:
        return 0.0

    common_words = problem_words.intersection(keyword_words)

    word_score = len(common_words) / len(keyword_words)

    text_score = SequenceMatcher(
        None,
        problem,
        keyword
    ).ratio()

    return max(word_score, text_score)


def semantic_diagnosis(problem: str):

    if not problem or not problem.strip():
        return {
            "problem_type": None,
            "score": 0.0
        }

    best_problem_type = None
    best_score = 0.0

    for problem_type, data in knowledge_base.items():

        for keyword in data["keywords"]:

            score = calculate_similarity(
                problem,
                keyword
            )

            if score > best_score:
                best_score = score
                best_problem_type = problem_type

    return {
        "problem_type": best_problem_type,
        "score": best_score
    }