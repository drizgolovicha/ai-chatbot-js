import hashlib
import os
import shutil
import pathlib
from dotenv import load_dotenv

load_dotenv()  # noqa: E402

from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.schema import Document
from langchain_chroma.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

from utils.docstore import SQLiteDocStore

# Path to the directory to save a Chroma database
root = pathlib.Path(__file__).parent.parent.resolve()
CHROMA_PATH = f"{root}/{os.environ.get('CHROMA_DIR')}"
DB_PATH = f"{root}/data/docs.sqlite"

global_unique_hashes = set()


def hash_text(text):
    """
    Generates a SHA-256 hash for the given input text.

    This function takes a string input, encodes it to bytes, computes its SHA-256
    hash using the hashlib library, and returns the resulting hash value in
    hexadecimal format. It can be used for applications that require hashing
    features like integrity validation, password storage, or data comparison.

    :param text: The input string to be hashed.
    :type text: str
    :return: The hexadecimal representation of the computed SHA-256 hash.
    :rtype: str
    """
    hash_object = hashlib.sha256(text.encode())
    return hash_object.hexdigest()


def split_text(documents: list[Document]):
    """
    Split the text content of the given list into smaller chunks.
    Args:
    documents (list[Document]): List of Document objects containing text content to split.
    Returns:
    list[Document]: List of Document objects representing the split text chunks.
    """
    # Initialize text splitter with specified parameters
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,  # Size of each chunk in characters
        chunk_overlap=100,  # Overlap between consecutive chunks
        length_function=len,  # Function to compute the length of the text
        add_start_index=True,  # Flag to add start index to each chunk
    )
    text_splitter = MarkdownTextSplitter(
        chunk_size=500,  # Size of each chunk in characters
        chunk_overlap=100,  # Overlap between consecutive chunks
        length_function=len,  # Function to compute the length of the text
    )

    """
    headers = [("#", "Header 1"),
               ("##", "Header 2"),
               ("###", "Header 3")]
    md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers, strip_headers=False)

    chunks = []
    for doc in documents:
        parsed_chunks = md_splitter.split_text(doc.page_content)
        for chunk in parsed_chunks:
            chunk.metadata['source'] = doc.metadata['source']
        chunks.extend(parsed_chunks)

    # Split documents into smaller chunks using text splitter
    # chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # Deduplication mechanism
    unique_chunks = []
    for chunk in chunks:
        chunk_hash = hash_text(chunk.page_content)
        if chunk_hash not in global_unique_hashes:
            unique_chunks.append(chunk)
            global_unique_hashes.add(chunk_hash)

    print(f"Unique chunks equals {len(unique_chunks)}.")
    return unique_chunks  # Return the list of split text chunks


def save_to_chroma(chunks: list[Document]):
    """
    Save the given list of Document objects to a Chroma database.
    Args:
    chunks (list[Document]): List of Document objects representing text chunks to save.
    Returns:
    None
    """
    # Clear out the existing database directory if it exists
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new Chroma database from the documents using OpenAI embeddings
    Chroma.from_documents(
        documents=chunks,
        embedding=OllamaEmbeddings(model="mxbai-embed-large"),
        persist_directory=CHROMA_PATH
    )

    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


def generate_data_store():
    """
    Function to generate vector database in chroma from documents.
    """
    try:
        db_conn = SQLiteDocStore(db_path=DB_PATH)
        docs_list = db_conn.list()
        chunks = split_text(docs_list)   # Split documents into manageable chunks
        save_to_chroma(chunks)  # Save the processed data to a data store
        db_conn.update_parsed_status([doc.metadata.get('id') for doc in docs_list])

    except BaseException as ex:
        print(str(ex))


if __name__ == "__main__":
    generate_data_store()
