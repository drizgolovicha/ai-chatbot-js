import json
import sqlite3
import uuid

from typing import List

from langchain_community.docstore.base import Docstore
from langchain.docstore.document import Document

from utils.index import generate_md5_hash


class SQLiteDocStore(Docstore):
    """
    SQLite-backed document store.

    Stores text, JSON metadata, MD5 hash and a parsed flag for each document.
    """
    def __init__(self, db_path="docs.sqlite"):
        """
        Initialize the store and ensure the table exists.

        :param db_path: Path to the SQLite database file.
        :type db_path: str
        """
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS docs (id TEXT PRIMARY KEY, text TEXT, metadata TEXT, hash TEXT(32), parsed BOOLEAN DEFAULT 0)"
        )

    def update_document(self, doc_id: str, doc: Document):
        """
        Update an existing document by id.

        Recomputes the MD5 hash from ``doc.page_content`` and sets ``parsed`` to 1.

        :param doc_id: Document identifier to update.
        :type doc_id: str
        :param doc: New document content and metadata.
        :type doc: Document
        :returns: None
        :rtype: None
        """
        self.conn.execute(
            """UPDATE docs SET
            text=?,
            metadata=?,
            parsed=1,
            hash=?
            WHERE id=?""",
            (doc.page_content, json.dumps(doc.metadata), generate_md5_hash(doc.page_content), doc_id))
        self.conn.commit()

    def add(self, doc: Document) -> str:
        """
        Insert a new document.

        Saves text, JSON metadata, computed MD5 hash, and sets ``parsed=0``.

        :param doc: Document to insert.
        :type doc: Document
        :returns: Generated UUID string of the new document.
        :rtype: str
        """
        doc_id = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO docs VALUES (?, ?, ?, ?, ?)",
            (doc_id, doc.page_content, json.dumps(doc.metadata), generate_md5_hash(doc.page_content), 0),
        )
        self.conn.commit()
        return doc_id

    def update_parsed_status(self, doc_ids: List[str]):
        """
        Mark multiple documents as parsed.

        :param doc_ids: List of document ids to set ``parsed=1``.
        :type doc_ids: List[str]
        :returns: None
        :rtype: None
        """
        placeholders = ','.join('?' for _ in doc_ids)
        self.conn.execute(f"UPDATE docs SET parsed=1 WHERE id IN ({placeholders})", tuple(doc_ids))
        self.conn.commit()

    def search(self, doc_id: str) -> Document:
        """
        Retrieve a document by id.

        :param doc_id: Document identifier to fetch.
        :type doc_id: str
        :returns: Document with text and metadata.
        :rtype: Document
        :raises KeyError: If the document is not found.
        """
        cur = self.conn.execute("SELECT text, metadata FROM docs WHERE id=?", (doc_id,))
        row = cur.fetchone()
        if row is None:
            raise KeyError(f"Doc {doc_id} not found")
        text, metadata = row
        return Document(page_content=text, metadata=json.loads(metadata))

    def list(self) -> List[Document]:
        """
        List all unparsed documents (``parsed=0``).

        Adds ``id`` to each document's metadata.

        :returns: Unparsed documents.
        :rtype: List[Document]
        """
        cur = self.conn.execute("SELECT text, metadata, id FROM docs WHERE parsed=0")
        docs = []
        for text, meta, fid in cur.fetchall():
            metadata = json.loads(meta)
            metadata['id'] = fid
            docs.append(Document(page_content=text, metadata=metadata))

        return docs

    def parsedList(self) -> List[Document]:
        """
        List all parsed documents (``parsed=1``).

        Adds ``id`` and ``hash`` to each document's metadata.

        :returns: Parsed documents.
        :rtype: List[Document]
        """
        cur = self.conn.execute("SELECT hash, text, metadata, id FROM docs WHERE parsed=1 limit 1")
        docs = []
        for doc_hash, text, meta, fid in cur.fetchall():
            metadata = json.loads(meta)
            metadata['id'] = fid
            metadata['hash'] = doc_hash
            docs.append(Document(page_content=text, metadata=metadata))

        return docs

    def truncate(self) -> None:
        """
        Delete all documents from the store.

        :returns: None
        :rtype: None
        """
        self.conn.execute("DELETE FROM docs")
        self.conn.commit()

    def delete(self, doc_id: str) -> None:
        """
        Delete a document by id.

        :param doc_id: Document identifier to remove.
        :type doc_id: str
        :returns: None
        :rtype: None
        """
        self.conn.execute("DELETE FROM docs WHERE id=?", (doc_id,))
        self.conn.commit()
