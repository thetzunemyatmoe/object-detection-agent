from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from sentence_transformers import SentenceTransformer


def chunk_documents(text, chunk_size=200, overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len
    )
    texts = text_splitter.split_text(text)
    return texts


def embed(documents):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(documents)


def save_to_vector_db(embeddings):
    client = chromadb.PersistentClient(path="data/vector_db")
    collection = client.create_collection(name="collection")
    collection.add(
        ids=[f"id{index}" for index in range(1, len(embeddings) + 1)],
        embeddings=embeddings
    )
