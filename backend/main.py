from fastapi import FastAPI
from pydantic import BaseModel
from utils.rag_engine import generate_answer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def get_answer(req: QueryRequest):
    result = generate_answer(req.query)
    return {"response": result}

@app.get("/")
async def root():
    return {"message": "✅ FastAPI backend is running successfully!"}
