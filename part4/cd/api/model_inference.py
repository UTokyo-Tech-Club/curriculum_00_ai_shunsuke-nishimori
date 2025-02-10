# model_inference.py

import os
import pandas as pd
from llama_index.core import VectorStoreIndex, Document, StorageContext
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from chromadb.config import Settings

# ファインチューニングや ChatCompletion API を利用する際は openai モジュールが必要になります
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数から API キーを取得（finetune.py などでの使い方を参考）
load_dotenv(verbose=True)
load_dotenv(".env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# CSV ファイルのパス（data/nihon_shokuhin.csv に、7列（食品名(100gあたり), エネルギー(kcal), 水分(g),
# たんぱく質(g), 脂質(g), 炭水化物(g), 食塩相当量(g)）の 2539 行のデータがある前提）
# このファイル(model_inference.py)があるディレクトリを取得
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_PATH = os.path.join(CURRENT_DIR, "nihon_shokuhin.csv")

def load_documents_from_csv(csv_path: str):
    """
    CSV ファイルから各行の食品栄養情報を読み込み、各行を1つのテキストにまとめた Document オブジェクトのリストを返す。
    ※ CSV は UTF-8 エンコーディングで、以下の列が存在する前提:
      - '食品名(100gあたり)'
      - 'エネルギー(kcal)'
      - '水分(g)'
      - 'たんぱく質(g)'
      - '脂質(g)'
      - '炭水化物(g)'
      - '食塩相当量(g)'
    """
    df = pd.read_csv(csv_path, encoding="utf-8")
    documents = []
    for idx, row in df.iterrows():
        text = (
            f"食品名(100gあたり): {row['食品名(100gあたり)']}\n"
            f"エネルギー(kcal): {row['エネルギー(kcal)']}\n"
            f"水分(g): {row['水分(g)']}\n"
            f"たんぱく質(g): {row['たんぱく質(g)']}\n"
            f"脂質(g): {row['脂質(g)']}\n"
            f"炭水化物(g): {row['炭水化物(g)']}\n"
            f"食塩相当量(g): {row['食塩相当量(g)']}"
        )
        documents.append(Document(text=text))
    return documents

# CSV から食品情報を読み込み、llama_index のインデックスを作成
documents = load_documents_from_csv(CSV_FILE_PATH)

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

def run_model(query: str) -> str:
    """
    ユーザーのクエリ（例："低カロリーでバランスの取れた晩御飯を提案して"）に基づき、
    以下の処理を行います:
      1. 作成済みの GPTSimpleVectorIndex から、関連する食品栄養情報をリトリーブする
      2. リトリーブ結果を含めたプロンプトを生成する
      3. openai.ChatCompletion API を用いて、プロンプトから今日の晩御飯提案（メニューとカロリー計算）を生成する
    """
    # ① リトリーブ（RAG 部分）
    retrieved = query_engine.query(query)
    
    # ② プロンプト作成
    prompt = (
        f"以下は日本食品標準成分表に基づく食品の栄養情報です:\n{retrieved}\n\n"
        f"上記情報を参考に、ユーザーのリクエスト「{query}」に沿った、今日の晩御飯のメニューと各食品のカロリー計算を、"
        "栄養士として詳しく提案してください。"
    )
    
    # ③ ChatCompletion API を使って回答生成
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "あなたはプロの栄養士兼料理研究家です。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000,
    )
    
    answer = response.choices[0].message.content
    return answer

if __name__ == "__main__":
    # テスト用：ローカルで動作確認する場合
    test_query = "低カロリーで栄養バランスの良い晩御飯の提案をしてください。"
    result = run_model(test_query)
    print("提案された晩御飯:")
    print(result)