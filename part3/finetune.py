from openai import OpenAI
import os
from dotenv import load_dotenv

# 環境変数からAPIキーを読み込む
load_dotenv(verbose=True)
load_dotenv(".env")

# OpenAIクライアントの初期化
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 学習用データのファイルパス
data_path = "dataset.jsonl"

# データセットのアップロード
file = client.files.create(
  file=open(data_path, "rb"),
  purpose="fine-tune"
)

# fine-tune jobの作成
fine_tuning_job = client.fine_tuning.jobs.create(
  training_file=file.id,
  model="gpt-4o-mini-2024-07-18"
)

# fine-tune jobのイベントの取得
finetune_data = client.fine_tuning.jobs.list_events(fine_tuning_job_id=fine_tuning_job.id)

print(finetune_data)