import lancedb
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.vectorstores import LanceDB
from langchain_text_splitters import RecursiveCharacterTextSplitter

from web.documents.utils.custom_embeddings import CustomEmbeddings
from pathlib import Path

def insert_document():

    base_dir = Path("./web/documents/source_file")

    documents = []

    for file_path in base_dir.rglob("*"):

        if file_path.suffix == ".txt":
            loader = TextLoader(str(file_path), encoding="utf-8")
            documents.extend(loader.load())

        elif file_path.suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))
            documents.extend(loader.load())

    print(f"加载文档数量: {len(documents)}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    texts = text_splitter.split_documents(documents)

    embeddings = CustomEmbeddings()

    db = lancedb.connect('./web/documents/lancedb_storage')

    vector_db = LanceDB.from_documents(
        documents=texts,
        embedding=embeddings,
        connection=db,
        table_name='my_knowledge_base',
        mode='overwrite',
    )

    print(f"已插入 {vector_db._table.count_rows()} 行数据")