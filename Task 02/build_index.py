import os
import time
from datasets import load_dataset
import lancedb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

DB_PATH = "./lancedb_data"
TABLE_NAME = "rag_knowledge"


def process_and_index():
    print("🚀 Step 1/3: Loading MSMARCO-XI dataset...")
    rows_data = []

    # Attempt to stream directly from raw jsonl; fallback to sample if network issues occur
    try:
        dataset = load_dataset(
            "json",
            data_files={
                "train": "hf://datasets/ai4bharat/MSMARCO-XI/train/hintrain.jsonl"
            },
            split="train[:150]",
        )
        for item in dataset:
            text = (
                item.get("Answer")
                or item.get("passage")
                or item.get("text")
                or ""
            )
            if text and len(text.strip()) > 20:
                rows_data.append(
                    {"id": str(item.get("id", len(rows_data))), "text": text}
                )
    except Exception as e:
        print(
            f"⚠️ Remote stream failed ({e}). Loading built-in dataset samples..."
        )
        sample_corpus = [
            (
                "doc_1",
                "Hacker House Goa 2026 is India's premier builder residency focusing on AI and Web3 innovation.",
            ),
            (
                "doc_2",
                "Retrieval Augmented Generation combines dense vector retrieval with low-latency language models.",
            ),
            (
                "doc_3",
                "To achieve sub-200ms latency in voice RAG systems, use in-memory vector indexing and streaming inference.",
            ),
            (
                "doc_4",
                "Sarvam AI and ElevenLabs provide low-latency speech recognition and voice generation APIs for Indic languages.",
            ),
            (
                "doc_5",
                "LanceDB provides serverless, embedded columnar vector storage with sub-10ms search times.",
            ),
            (
                "doc_6",
                "Guardrails in AI systems inspect input queries to prevent prompt injection and verify factual groundedness.",
            ),
            (
                "doc_7",
                "Hierarchical parent-child chunking indexes small sentence units while passing wider context to the LLM.",
            ),
            (
                "doc_8",
                "MSMARCO-XI is an Indic multilingual retrieval dataset translated across major Indian languages.",
            ),
        ]
        rows_data = [{"id": doc_id, "text": text} for doc_id, text in sample_corpus]

    print(f"✅ Loaded {len(rows_data)} source records.")

    print(
        "🧠 Step 2/3: Initializing embedding model & Hierarchical Splitters..."
    )
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    # Hierarchical splitters
    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=450,
        chunk_overlap=40,
        separators=["\n\n", "\n", "। ", ". ", " "],
    )
    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=120, chunk_overlap=15, separators=["\n", "। ", ". ", " "]
    )

    data_to_insert = []
    start_time = time.perf_counter()

    for row in rows_data:
        doc_id = row["id"]
        full_text = row["text"]
        parent_chunks = parent_splitter.split_text(full_text)

        for p_idx, p_chunk in enumerate(parent_chunks):
            child_chunks = child_splitter.split_text(p_chunk)
            for c_idx, c_chunk in enumerate(child_chunks):
                vector = embed_model.encode(c_chunk).tolist()
                data_to_insert.append(
                    {
                        "vector": vector,
                        "id": f"{doc_id}_{p_idx}_{c_idx}",
                        "text": c_chunk,
                        "parent_context": p_chunk,
                        "source": "msmarco-xi",
                    }
                )

    print("💾 Step 3/3: Writing vector records to LanceDB...")
    db = lancedb.connect(DB_PATH)
    db.create_table(TABLE_NAME, data=data_to_insert, mode="overwrite")

    duration = round((time.perf_counter() - start_time), 2)
    print(f"\n===========================================")
    print(f"🎉 Indexing complete in {duration}s!")
    print(f"📊 Indexed {len(data_to_insert)} chunks in {DB_PATH}")
    print(f"===========================================\n")


if __name__ == "__main__":
    process_and_index()