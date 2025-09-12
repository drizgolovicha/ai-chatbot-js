from langchain_chroma.vectorstores import Chroma


def delete_by_sources(db: Chroma, sources: list[str]) -> None:
    """
    Delete all vectors from Chroma where metadata["source"] == source.

    :param db: Chroma instance
    :param sources: The value of metadata["source"] to filter by
    """
    collection = db._collection  # low-level chromadb API
    collection.delete(where={"source": {"$in": sources}})
    print(f"All vectors with source $in '{sources}' deleted successfully.")
