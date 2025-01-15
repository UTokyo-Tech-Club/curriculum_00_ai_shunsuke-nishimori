"""
!pip install llama-index
!pip install llama-index-embeddings-openai
!pip install llama-index-vector-stores-chroma
!pip install llama-index-llms-openai
!pip install ipywidgets
!pip install chromadb
!pip install PyMuPDF
"""
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from chromadb.config import Settings
from llama_index.readers.file import PyMuPDFReader

# 環境変数からAPIキー（OPENAI_API_KEY）を読み込む
load_dotenv(verbose=True)
load_dotenv(".env")

# PDFファイルの読み込み
pdf_reader = PyMuPDFReader()
pdf_documents = pdf_reader.load(file_path="./ragjoho.pdf")

# JSONLファイルの読み込み
json_documents = SimpleDirectoryReader(input_files=["./ragdata.jsonl"]).load_data()

# ドキュメントの統合
documents = pdf_documents + json_documents

# ChromaDBの設定
persist_directory = "chroma_db"
chroma_client = chromadb.Client(Settings(persist_directory=persist_directory))
chroma_collection = chroma_client.get_or_create_collection(name="rag_collection")

# Vector Storeの作成
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# インデックスの作成
node_parser = SimpleNodeParser()
nodes = node_parser.get_nodes_from_documents(documents)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes=nodes, storage_context=storage_context)

# クエリエンジンの作成
query_engine = index.as_query_engine()

# クエリの実行
query_str_list = [
    "AIに対する英国の反応は？",
    "日本郵政グループの構成は？"
    "Beyond 5Gを取り巻く国内外の動向は？",
    "企業・公共団体等における生成 AI 導入動向は？",
    "AIに関する国内外の規制動向は？",
]
for query_str in query_str_list:
    response = query_engine.query(query_str)
    print(response)
