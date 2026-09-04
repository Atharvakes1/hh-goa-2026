import os
import time
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import lancedb
import numpy as np
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

app = FastAPI(title="HH Goa 2026 Voice RAG")

print("⚡ Loading in-memory models...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
db = lancedb.connect("./lancedb_data")
table = db.open_table("rag_knowledge")

latency_history = []
groq_client = None

if GROQ_API_KEY:
    try:
        from groq import Groq
        groq_client = Groq(api_key=GROQ_API_KEY)
    except Exception:
        groq_client = None

class QueryRequest(BaseModel):
    query: str

def pre_retrieval_guardrail(query: str) -> tuple[bool, str]:
    blocked_keywords = ["weather", "cricket score", "movie ticket", "hack bank"]
    for kw in blocked_keywords:
        if kw in query.lower():
            return False, f"Query contains out-of-scope keyword: '{kw}'. Request blocked."
    if len(query.strip()) < 3:
        return False, "Query too short."
    return True, "Passed"

def post_retrieval_groundedness(query: str, retrieved_context: list[str]) -> bool:
    return len(retrieved_context) > 0

@app.post("/api/rag")
async def execute_rag(req: QueryRequest):
    t_start = time.perf_counter()

    is_safe, reason = pre_retrieval_guardrail(req.query)
    if not is_safe:
        return {
            "answer": reason,
            "guardrail_status": "BLOCKED",
            "retrieval_time_ms": 0.0,
            "total_latency_ms": round((time.perf_counter() - t_start) * 1000, 2)
        }

    t_ret_start = time.perf_counter()
    query_vector = embed_model.encode(req.query).tolist()
    results = table.search(query_vector).limit(3).to_list()
    retrieval_time = round((time.perf_counter() - t_ret_start) * 1000, 2)

    contexts = [r["parent_context"] for r in results]
    context_str = "\n".join(contexts)

    grounded = post_retrieval_groundedness(req.query, contexts)

    if groq_client:
        prompt = f"Answer the user query strictly using the provided context.\nContext:\n{context_str}\n\nQuery: {req.query}\nAnswer:"
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.1
        )
        answer = completion.choices[0].message.content
    else:
        answer = contexts[0] if contexts else "No direct match found in MSMARCO knowledge base."

    total_latency = round((time.perf_counter() - t_start) * 1000, 2)
    latency_history.append(total_latency)

    lat_arr = np.array(latency_history)
    metrics = {
        "p50": round(float(np.percentile(lat_arr, 50)), 1),
        "p70": round(float(np.percentile(lat_arr, 70)), 1),
        "p100": round(float(np.percentile(lat_arr, 100)), 1),
        "count": len(latency_history)
    }

    return {
        "query": req.query,
        "answer": answer,
        "guardrail_status": "PASSED" if grounded else "UNVERIFIED",
        "retrieval_time_ms": retrieval_time,
        "total_latency_ms": total_latency,
        "telemetry": metrics
    }

os.makedirs("static", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)