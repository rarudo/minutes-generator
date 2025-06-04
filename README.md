# 議事録生成システム

Gemini 2.5 Flash API を使用して音声ファイルの文字起こしを行い、
議事録を自動生成するツールです。

## 前提条件
- Python 3.9+
- [uv](https://docs.astral.sh/uv/) (Pythonパッケージマネージャー)
- Google Cloudプロジェクト
- Vertex AI API有効化

## セットアップ

### 1. uvのインストール
uvがインストールされていない場合、以下のコマンドでインストールします：
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. プロジェクトの依存関係インストール
```bash
uv sync
```

### 3. 環境変数の設定
`.env-sample` を `.env` にコピーし、 `GOOGLE_API_KEY` を設定します:
```bash
cp .env-sample .env
# .env を編集して API キーを記入
```
またはシェルで直接指定します:
```bash
export GOOGLE_API_KEY="your-api-key"
```

## 使い方
音声ファイル (m4a/mp3/wav/ogg/flac) を指定して実行します:

```bash
uv run python -m minutes_generator path/to/audio_file.m4a
```

または、スクリプトとして実行：
```bash
uv run minutes-generator path/to/audio_file.m4a
```

起動後はチャット形式で操作できます：
- `/exit`: プログラムを終了
- `/copy`: 最新の議事録をクリップボードへコピー
- その他のテキスト: 議事録の修正指示

## グローバルインストール（推奨）
uvツールを使ってシステム全体で使えるコマンドとしてインストールできます：

```bash
# プロジェクトディレクトリで実行
uv tool install .
```

インストール後は、どこからでも直接コマンドを実行できます：
```bash
# どのディレクトリからでも実行可能
minutes-generator path/to/audio_file.m4a
```

### グローバルインストールの管理
```bash
# アップデート（プロジェクトディレクトリで実行）
uv tool install --force .

# アンインストール
uv tool uninstall minutes-generator

# インストール済みツールの確認
uv tool list
```

## プロジェクト構造
- `pyproject.toml`: プロジェクト設定と依存関係管理
- `uv.lock`: 依存関係の正確なバージョンロック
- `system_prompt.txt`: 議事録の生成形式を指定するシステムプロンプト
- `minutes_generator/`: メインアプリケーションコード
- `.env`: APIアクセス用の環境変数（要作成）

## 開発者向け

### 新しい依存関係の追加
```bash
uv add package-name
```

### 開発用依存関係の追加
```bash
uv add --dev package-name
```

### Pythonバージョンの確認
```bash
uv run python --version
```

## カスタマイズ
- `system_prompt.txt`: 議事録の生成形式を指定するシステムプロンプト
- `minutes_generator/config.py`: リトライ回数やモデル名などの設定
- `.env`: APIアクセス用の環境変数
