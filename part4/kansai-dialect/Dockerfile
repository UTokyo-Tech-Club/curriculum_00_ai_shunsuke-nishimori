# python3.9のイメージをダウンロード
FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /src

# pipを使ってpoetryをインストール
RUN pip install poetry

# poetryの定義ファイルをコピー (存在する場合)
COPY pyproject.toml* poetry.lock* ./

# poetryでライブラリをインストール (pyproject.tomlが既にある場合)
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

# ファイルをコピー
COPY . .

# postリクエストを送るとchatgptによる返答を返すappを起動
CMD [".venv/bin/uvicorn", "main:app", "--host", "0.0.0.0"]

# 以下のコマンドでDockerイメージをビルド
# docker build -t kansai-dialect .
# 以下のコマンドでDockerコンテナを起動
# docker run -p 5000:5000 kansai-dialect
# 以下のコマンドでDockerコンテナを停止
# docker stop kansai-dialect
# 以下のコマンドでDockerコンテナを削除
# docker rm kansai-dialect
# 以下のコマンドでDockerイメージを削除
# docker rmi kansai-dialect