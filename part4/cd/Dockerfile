# Dockerfile
FROM --platform=linux/amd64 python:3.10
ENV PYTHONUNBUFFERED=1

# 追加：ソースコードのルート (/src) をモジュール検索パスに追加
ENV PYTHONPATH=/src

WORKDIR /src

# RUN apt-get update && apt-get install -y gcc python3-dev libffi-dev build-essential && rm -rf /var/lib/apt/lists/*

# pipを使ってpoetryをインストール
RUN pip install poetry

# poetryの定義ファイルをコピー (存在する場合)
COPY pyproject.toml* poetry.lock* ./

# poetryでライブラリをインストール (pyproject.tomlが既にある場合)
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

# greenlet の C 拡張をソースから強制ビルドする
RUN poetry run pip install --force-reinstall --no-binary :all: greenlet==3.1.1

# ソースコードをすべてコピー
COPY . .

# DBマイグレーションの実行は手動で行うしかない？
# RUN poetry run python api/migrate_db.py

# uvicornのサーバーを立ち上げる
ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]