from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Location of the AquaGuard knowledge base
KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "data" / "knowledge"


def load_knowledge_documents():
    """
    Load all .txt documents from the AquaGuard knowledge directory.
    """

    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):
        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )

        file_documents = loader.load()

        for document in file_documents:
            document.metadata["source"] = file_path.name

        documents.extend(file_documents)

    return documents


def split_documents(documents):
    """
    Split knowledge documents into smaller chunks
    suitable for retrieval.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    return chunks


if __name__ == "__main__":

    documents = load_knowledge_documents()

    print(f"Documents loaded: {len(documents)}")

    for document in documents:
        print(f"Loaded: {document.metadata['source']}")

    chunks = split_documents(documents)

    print(f"\nTotal chunks created: {len(chunks)}")

    print("\nExample chunk:")
    print("--------------------------------")
    print(chunks[0].page_content)
    print("--------------------------------")
    print("Source:", chunks[0].metadata["source"])