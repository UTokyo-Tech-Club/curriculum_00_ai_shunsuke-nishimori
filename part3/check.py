from openai import OpenAI
import time
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
load_dotenv(".env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ファインチューニングジョブのIDを指定
JOB_ID = "ftjob-rVtQRdpeyJ82HRyktZymh8ee"  # ここを実際のジョブIDに変更

def check_job_status(job_id):
    """ジョブのステータスを確認する"""
    print(f"ジョブ {job_id} のステータスを確認しています...")
    try:
        response = client.fine_tuning.jobs.retrieve(job_id)
        status = response['status']
        print(f"現在のジョブステータス: {status}")
        return status, response.get("fine_tuned_model")
    except Exception as e:
        print(f"ジョブステータス確認エラー: {e}")
        return None, None

def wait_for_job_completion(job_id):
    """ジョブが完了するまで待機"""
    while True:
        status, fine_tuned_model = check_job_status(job_id)
        if status == "succeeded":
            print("ジョブが成功しました！")
            return fine_tuned_model
        elif status == "failed":
            print("ジョブが失敗しました。")
            return None
        print("ジョブがまだ完了していません。30秒後に再確認します...")
        time.sleep(30)

def use_fine_tuned_model(model_name):
    """ファインチューニング済みモデルを使用する"""
    if not model_name:
        print("モデル名が無効です。")
        return

    print(f"ファインチューニング済みモデル '{model_name}' を使用しています...")
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "UTTCに関する質問に回答します。"},
                {"role": "user", "content": "UTTCのValueを3つ挙げてください。"}
            ]
        )
        print("モデルの応答:")
        print(response['choices'][0]['message']['content'])
    except Exception as e:
        print(f"モデル利用エラー: {e}")

def main():
    # ジョブのステータスを確認し、成功するまで待機
    fine_tuned_model = wait_for_job_completion(JOB_ID)
    
    if fine_tuned_model:
        # モデルを使用する
        use_fine_tuned_model(fine_tuned_model)
    else:
        print("ジョブが成功しなかったため、モデルを使用できません。")

if __name__ == "__main__":
    main()