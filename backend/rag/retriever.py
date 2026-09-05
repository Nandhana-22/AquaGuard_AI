from pathlib import Path
import pickle

import faiss
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent
VECTOR_DIR = BASE_DIR / "vector_store"

INDEX_PATH = VECTOR_DIR / "aquaguard.index"
CHUNKS_PATH = VECTOR_DIR / "chunks.pkl"


print("Loading FAISS index...")
index = faiss.read_index(str(INDEX_PATH))

print("Loading knowledge chunks...")
with open(CHUNKS_PATH, "rb") as f:
    chunks = pickle.load(f)

print(f"Knowledge chunks loaded: {len(chunks)}")


print("Loading embedding model...")
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded.")


def retrieve_knowledge(query, top_k=3):

    query_embedding = model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    distances, indices = index.search(
        query_embedding.reshape(1, -1).astype("float32"),
        top_k
    )

    results = []

    for distance, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        chunk = chunks[idx]

        results.append({
            "content": chunk.page_content,
            "source": chunk.metadata.get("source", "unknown"),
            "distance": float(distance)
        })

    return results


if __name__ == "__main__":

    query = "What should I check if water consumption remains unusually high?"

    print("\n================================")
    print("AquaGuard RAG Retrieval Test")
    print("================================")

    print(f"\nQuery: {query}\n")

    results = retrieve_knowledge(query, top_k=3)

    for i, result in enumerate(results, start=1):

        print(f"--- Result {i} ---")
        print(f"Source: {result['source']}")
        print(f"Distance: {result['distance']:.4f}")
        print(result["content"])
        print()