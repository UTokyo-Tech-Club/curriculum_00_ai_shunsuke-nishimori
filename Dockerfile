# ベースイメージとしてPython 3.12を使用
FROM python:3.12-slim-bookworm

# ビルド環境にuvをインストール
RUN pip install uv

# uvをコピー
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY pyproject.toml uv.lock ./

# 依存関係をインストール
RUN uv sync --frozen --compile-bytecode --group dev

# Jupyter Labを開発環境としてインストール
RUN uv add --dev jupyterlab ipykernel

# プロジェクトのカーネルを作成
RUN uv run ipython kernel install --user --name=your_project

# ポートを公開
EXPOSE 8888

# Jupyter Labを起動
CMD ["uv", "run", "--with", "jupyter", "jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]