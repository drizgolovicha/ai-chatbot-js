import os
import pathlib
import sys
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()  # noqa: E402

from langchain_chroma.vectorstores import Chroma
from utils.chroma import delete_by_sources
from utils.index import generate_md5_hash, split_text
from utils.docstore import SQLiteDocStore
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import MarkdownifyTransformer, BeautifulSoupTransformer
from langchain_ollama import OllamaEmbeddings

# Path to the directory to save a Chroma database
root = pathlib.Path(__file__).parent.parent.resolve()
FILE_TO_PARSE = f"{root}/data/links.txt"
DB_PATH = f"{root}/data/docs.sqlite"
CHROMA_PATH = f"{root}/{os.environ.get('CHROMA_DIR')}"

db_conn = SQLiteDocStore(db_path=DB_PATH)
chroma = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=OllamaEmbeddings(model="mxbai-embed-large")
)


def asyncLoader():
    """
    Method to get all parsed list, after get source and compare md5 hash
    - Load parsed list
    - Load page source
    - Compare md5 hash
    - If hashes not equal, remove relate vectors
    - Put new vectors
    :return:
    """
    parsed_docs = db_conn.parsedList()
    hash_map = {}
    for doc in parsed_docs:
        hash_map[doc.metadata.get('source')] = doc.metadata

    print(f"Found {len(parsed_docs)} parsed documents")

    loader = AsyncHtmlLoader([doc.metadata.get('source') for doc in parsed_docs])
    docs = loader.load()

    # Transform
    bs_transformer = BeautifulSoupTransformer()

    for doc in docs:
        doc.page_content = bs_transformer.remove_unwanted_tags(doc.page_content, ['head', 'iframe', 'svg', 'picture', 'noscript', 'link', 'footer',
                                                                                  'script', 'img', 'style', 'button'])
        doc.page_content = bs_transformer.remove_unwanted_classnames(doc.page_content,
                                                                     ['blog-rec', 'cta-post', 'main-nav', 'search-panel', 'social-panel',
                                                                      'widget-block', 'modal-layer', 'cmplz-cookiebanner', 'breadcrumbs',
                                                                      'page-form__content', 'post-date'])

        doc.page_content = bs_transformer.remove_unnecessary_lines(doc.page_content)

    md = MarkdownifyTransformer()
    docs_transformed = md.transform_documents(docs)

    # Compare md5 hash
    docs2update = []
    hash_keys = hash_map.keys()
    for doc in docs_transformed:
        md5_hash = generate_md5_hash(doc.page_content)

        # check we have parsed source
        if doc.metadata.get('source') not in hash_keys:
            print(f"The source '{doc.metadata.get('source')}' does not exist in parsed database, added to replace")
            docs2update.append(doc)
            continue

        # check hashes
        if md5_hash != hash_map[doc.metadata.get('source')].get('hash'):
            print(f"md5 hashes do not match for source '{doc.metadata.get('source')}', added to replace")
            docs2update.append(doc)
            continue

    if len(docs2update) < 1:
        print('Nothing to parse, exit script')
        sys.exit()

    print(f'Found {len(docs2update)} documents to be replaced')

    # remove obsolete vectors
    page_sources = [doc.metadata.get('source') for doc in docs2update]
    delete_by_sources(chroma, page_sources)

    # form new vectors
    vectors = split_text(docs2update)
    chroma.add_documents(vectors)
    print(f'{len(vectors)} vectors were added')

    # Update md5 for parsed docs
    for doc in docs2update:
        metadata = hash_map[doc.metadata.get('source')]
        db_conn.update_document(metadata.get('id'), doc)

    print(f'DB documents are updated')


if __name__ == "__main__":
    print(f'{str(datetime.today())}')
    asyncLoader()
    print('\r\n\r\n')
