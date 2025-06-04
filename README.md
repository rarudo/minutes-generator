# 議事録生成システム

音声ファイルから議事録を自動生成し、チャット形式で修正・調整できるツールです。Google Gemini APIを使用して高精度な文字起こしと構造化された議事録を作成します。

## セットアップ

### 1. uvのインストール
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

### 3. Google API キーの設定
API キーを環境変数に設定します：

```bash
export GOOGLE_API_KEY="your-api-key"
```

または `.env` ファイルを作成：
```bash
echo "GOOGLE_API_KEY=your-api-key" > .env
```

## 使い方

### 基本的な実行方法
音声ファイルを指定してツールを起動：

```bash
uv run python -m minutes_generator path/to/audio_file.m4a
```

または：
```bash
uv run minutes-generator path/to/audio_file.m4a
```

### サポートされている音声形式
- m4a
- mp3
- wav
- ogg
- flac

### チャット操作
起動後はチャット形式で議事録を修正できます：

- **`/exit`** - プログラムを終了
- **`/copy`** - 議事録をクリップボードにコピー
- **その他のテキスト** - 議事録の修正指示（例：「参加者を追加して」「もっと詳しく書いて」）

### 使用例
```bash
# 音声ファイルから議事録を生成
$ uv run minutes-generator meeting.m4a

# 議事録が生成されたら、チャットで修正
> 佐藤さんの発言をもっと詳しく書いて
> タスクの担当者を明確にして
> /copy
```

## グローバルインストール（推奨）

システム全体で使えるコマンドとしてインストール：

```bash
uv tool install .
```

インストール後はどこからでも実行可能：
```bash
minutes-generator path/to/audio_file.m4a
```

### グローバルインストールの管理
```bash
# アップデート
uv tool install --force .

# アンインストール
uv tool uninstall minutes-generator

# インストール済みツールの確認
uv tool list
```

## カスタマイズ

### 議事録の形式を変更
`system_prompt.md` ファイルを編集することで、議事録の生成形式をカスタマイズできます。

### 設定の調整
`minutes_generator/config.py` でリトライ回数やその他の設定を調整できます。