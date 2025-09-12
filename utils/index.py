import os
import pathlib
import hashlib

from glob import glob
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_community.document_loaders import TextLoader, Docx2txtLoader
from langchain_core.documents.base import Document
from typing import List
from langchain.text_splitter import MarkdownHeaderTextSplitter


root = pathlib.Path(__file__).parent.parent.resolve()
DIALOGS_PATH = f"{root}/dialogs"


def generate_md5_hash(input_string: str) -> str:
    """
    Generates the MD5 hash of a given string.
    The input string is encoded to bytes using UTF-8 before hashing.
    """
    md5_hash_object = hashlib.md5()
    md5_hash_object.update(input_string.encode('utf-8'))
    return md5_hash_object.hexdigest()


def get_user_conversation(history: List[BaseMessage]):
    """
    Filter chat conversation, leaving the only query answer section
    :param history:
    :return: list
    """
    return [item for item in history if isinstance(item, (HumanMessage, AIMessage))]


def store_dialogs(session: str, history: list):
    """
    Append log message to existing log
    :param session:
    :param history:
    :return:
    """
    conversation = get_user_conversation(history)[-2:]
    today = datetime.now().strftime("%Y%m%d")

    with open(f'{DIALOGS_PATH}/{today}-{session[:8]}-headless.md', 'a') as file:
        file.write('```dialog\n')
        file.write('### USER\n')
        file.write(f'{conversation[0].content.strip()}\n')
        file.write('### ASSISTANT\n')
        file.write(f'{conversation[1].content.strip()}\n')
        file.write('```\n\n')


def get_finished_headless_dialogs() -> list[str]:
    """
    Returns a list of headless dialogue log file paths that haven't been modified in the last 24 hours.

    The function searches for all Markdown files in the DIALOGS_PATH directory that match the
    '*-headless.md' pattern. It filters out files modified within the last 24 hours, returning only those
    considered "finished" (i.e., older than 1 day).

    :return: List of file paths to finished headless dialogue logs.
    """

    pattern = f'{DIALOGS_PATH}/*-headless.md'
    matched_files = glob(pattern)

    files = []
    for file_path in matched_files:
        modified = os.path.getmtime(file_path)
        days_pass = (datetime.now() - datetime.fromtimestamp(modified)).days
        if days_pass > 0:
            files.append(file_path)

    return files


def prepend_to_file(file_path: str, text_to_prepend: str):
    """
    Prepends a given text block to the beginning of a file and renames the file if it matches a specific pattern.

    This function reads the original contents of a file, adds the provided text at the top, writes the new
    content back to the file, and renames the file by removing the '-headless' suffix if present.

    :param file_path: Path to the original file (expected to be a Markdown file).
    :param text_to_prepend: Text to insert at the beginning of the file content.
    :raises FileNotFoundError: If the given file does not exist.
    :raises Exception: If any other error occurs during file operations.
    """
    try:
        with open(file_path, 'r') as f:
            original_content = f.read()

        new_content = text_to_prepend + '\n\n' + original_content

        # Write the combined content back to the file
        with open(file_path, 'w') as f:
            f.write(new_content)

        updated_file_path = file_path.replace('-headless.md', '.md')
        os.rename(file_path, updated_file_path)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def pretty_print_docs_with_score(docs):
    """
    Prints a list of documents along with their similarity scores in a visually separated format.

    Each entry includes:
    - Similarity score
    - Document ID
    - Document content

    :param docs: A list of (Document, score) tuples, where:
                 - Document has `.id` and `.page_content` attributes
                 - score is a float representing similarity or relevance
    """
    print(
        f"\n{'-' * 100}\n".join(
            [f"Score: {d[1]}\n\n Document: {d[0].id}\n\n" + d[0].page_content for d in docs]
        )
    )


def pretty_print_docs(docs):
    """
    Nicely formats and prints a list of document chunks to the console.
    Each document's source (from metadata) and its content are printed with a visual separator between them.

    :param docs: A list of documents, each expected to have 'metadata["source"]' and 'page_content' attributes.
    """
    print(
        f"\n{'-' * 100}\n".join(
            [f"Document: {d.metadata.get('source')}\n\n" + d.page_content for d in docs]
        )
    )


def walk_through_files(path: str, file_extension='.txt'):
    """
    Recursively yields file paths from the given directory that match the specified extension.

    Walks through all subdirectories of the given `path` and yields the full path
    of each file that ends with the specified `file_extension`.

    Parameters:
        path (str): Root directory to start searching from.
        file_extension (str, optional): File extension to filter by. Defaults to '.txt'.

    Yields: str: Full path to each matching file.
    """
    for (dir_path, dir_names, filenames) in os.walk(path):
        for filename in filenames:
            if filename.endswith(file_extension):
                yield os.path.join(dir_path, filename)


def load_documents(data_path: str, extension='.txt') -> List[Document]:
    """
    Loads documents from files in the specified directory.

    Recursively traverses all files in the `data_path` directory,
    loads them using `TextLoader`, and returns a list of `Document` objects.

    Parameters:
        data_path (str): Path to the directory containing the files.
        extension (str, optional): File extension to load.
                                   Defaults to '.txt'.

    Returns: List[Document]: A list of loaded documents.
    """
    documents = []
    for f_name in walk_through_files(data_path, extension):
        if extension.endswith('docx'):
            document_loader = Docx2txtLoader(f_name)
        else:
            document_loader = TextLoader(f_name, encoding="utf-8")
        documents.extend(document_loader.load())

    return documents


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
    global_unique_hashes = set()
    # Initialize text splitter with specified parameters
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


PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'
