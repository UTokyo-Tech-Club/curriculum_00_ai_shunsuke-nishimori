# fastapiを使ってChatGPTを使った関西弁対話APIを作成する

from fastapi import FastAPI, APIRouter
from openai import OpenAI
import time
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import uvicorn

# 環境変数からAPIキーを読み込む
load_dotenv(verbose=True)
load_dotenv(".env")

# OpenAIクライアントの初期化
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

router = APIRouter()

# リクエストのモデルを定義
class ChatRequest(BaseModel):
    input: str

# レスポンスのモデルを定義
class ChatResponse(BaseModel):
    input: str
    output: str

# 今回のappではpostリクエストのみ使用。postリクエストで/chatにリクエストを送ると、関西弁で返答が返ってくる。
def chat(input: str):
    messages = [
        {"role": "system", "content": "コテコテの関西弁を話す中年のおばさんになりきって回答します。"},
        {"role": "user", "content": input}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages
    )
    return response.choices[0].message.content

@app.post("/chat", response_model=ChatResponse)
async def chat_api(request: ChatRequest):
    input = request.input
    output = chat(input)
    return ChatResponse(input=input, output=output)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Cloud Run の環境変数PORTを取得
    print(f"Starting server on port {port}...")  # ログ出力で確認
    uvicorn.run(app, host="0.0.0.0", port=port)