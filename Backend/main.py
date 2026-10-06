import os

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from diagnosis import diagnose_problem
from services.vision import analyze_image
from retrieval import retrieve_knowledge

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(
    title="ITERA",
    description="AI-Powered IT Self-Service Assistant",
    version="1.0.0"
)
FRONTEND_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "Frontend"
)

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProblemRequest(BaseModel):
    problem: str


@app.get("/")
def home():
    return FileResponse(
        os.path.join(FRONTEND_DIR, "index.html")
    )

@app.post("/diagnose")
def diagnose(request: ProblemRequest):

    result = diagnose_problem(request.problem)

    return {
        "problem": request.problem,
        "result": result
    }


@app.post("/analyze-image")
async def analyze_image_endpoint(
    file: UploadFile = File(...)
):

    image_path = f"temp_{file.filename}"

    try:

        with open(image_path, "wb") as buffer:
            buffer.write(await file.read())

        image_result = analyze_image(image_path)

        if not image_result["success"]:
            return image_result

        diagnosis = diagnose_problem(
            image_result["text"]
        )

        return {
            "image_analysis": image_result,
            "diagnosis": diagnosis
        }

    finally:

        if os.path.exists(image_path):
            os.remove(image_path)


@app.post("/retrieve")
def retrieve(problem: ProblemRequest):

    results = retrieve_knowledge(
        problem.problem
    )

    return {
        "problem": problem.problem,
        "results": results
    }