from pathlib import Path
import pickle

import faiss
from sentence_transformers import SentenceTransformer

from loader import load_knowledge_documents, split_documents


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
VECTOR_DIR = BASE_DIR / "vector_store"

VECTOR_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# Load embedding model
# --------------------------------------------------

print("Loading embedding model...")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded.")


# --------------------------------------------------
# Load and split AquaGuard knowledge
# --------------------------------------------------

documents = load_knowledge_documents()

chunks = split_documents(documents)

print(f"Total chunks: {len(chunks)}")


# --------------------------------------------------
# Extract text
# --------------------------------------------------

texts = [
    chunk.page_content
    for chunk in chunks
]


# --------------------------------------------------
# Create embeddings
# --------------------------------------------------

print("Creating embeddings...")

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=True
)


# --------------------------------------------------
# Create FAISS index
# --------------------------------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings.astype("float32"))


# --------------------------------------------------
# Save FAISS index
# --------------------------------------------------

index_path = VECTOR_DIR / "aquaguard.index"

faiss.write_index(
    index,
    str(index_path)
)


# --------------------------------------------------
# Save document chunks
# --------------------------------------------------

chunks_path = VECTOR_DIR / "chunks.pkl"

with open(chunks_path, "wb") as f:
    pickle.dump(chunks, f)


# --------------------------------------------------
# Output
# --------------------------------------------------

print("\n================================")
print("AquaGuard Vector Store Created")
print("================================")

print(f"Chunks indexed: {len(chunks)}")
print(f"Embedding dimension: {dimension}")
print(f"FAISS index: {index_path}")
print(f"Chunks file: {chunks_path}")