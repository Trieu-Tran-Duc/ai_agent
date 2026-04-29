from fastapi import FastAPI
from app.workflows.pipeline import run_pipeline

app = FastAPI()

@app.get("/analyze")
def analyze(keyword: str = "bitcoin"):
    return run_pipeline(keyword)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)