#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interactive Minutes Generator
Gemini-2.5-Flash-Preview-04-17 + google-genai v1.15
"""

import argparse
import os
import re
import sys
from contextlib import suppress

from dotenv import load_dotenv
from google import genai
from google.genai import types
import pyperclip
from rich.console import Console
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.history import FileHistory


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # -----------------------------------------------------------
    # 0) I/O 文字コードを UTF-8 に固定（Backspace 残り対策）
    # -----------------------------------------------------------
    with suppress(AttributeError):  # Python <3.7 は reconfigure 不可
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8")

    # -----------------------------------------------------------
    # 1) API キー読み込み & クライアント初期化
    # -----------------------------------------------------------
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        sys.exit("ERROR: .env に GOOGLE_API_KEY が見つかりません")

    client = genai.Client(api_key=api_key)
    model_id = "gemini-2.5-flash-preview-05-20"

    # -----------------------------------------------------------
    # 2) コマンドライン引数
    # -----------------------------------------------------------
    parser = argparse.ArgumentParser(
        description="Interactive minutes generator with Gemini 2.5 Flash Preview"
    )
    parser.add_argument("audio", help="Audio file path (m4a/mp3/wav/ogg/flac)")
    args = parser.parse_args(argv)

    audio_path = args.audio
    if not os.path.exists(audio_path):
        sys.exit(f"ERROR: {audio_path} が見つかりません")

    # -----------------------------------------------------------
    # 3) Rich Console ― 折り返し禁止で全文表示
    # -----------------------------------------------------------
    console = Console(width=None)

    # -----------------------------------------------------------
    # 4) 音声ファイルをアップロード
    # -----------------------------------------------------------
    with console.status("[bold blue]Uploading audio…"):
        try:
            uploaded_file = client.files.upload(file=audio_path)
        except Exception as exc:
            sys.exit(f"Upload failed: {exc}")

    # -----------------------------------------------------------
    # 5) system_prompt.md を読み込み
    # -----------------------------------------------------------
    try:
        system_prompt = open("system_prompt.md", encoding="utf-8").read()
    except FileNotFoundError:
        sys.exit("ERROR: system_prompt.md がありません")

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_LOW_AND_ABOVE",
            )
        ],
    )

    # -----------------------------------------------------------
    # 6) チャットセッションを開始
    # -----------------------------------------------------------
    chat = client.chats.create(model=model_id, config=config)

    def stream_request(parts):
        """Gemini にリクエストを送りストリーム出力を返す"""
        full = ""
        for chunk in chat.send_message_stream(parts):
            full += chunk.text
        console.print(full, no_wrap=True, overflow="ignore")
        return full.strip()

    # -----------------------------------------------------------
    # 7) 初回議事録生成
    # -----------------------------------------------------------
    console.rule("[bold green]Generating initial minutes")
    initial_xml = stream_request(
        ["この音声ファイルに基づいて議事録を作成してください。", uploaded_file]
    )
    latest_xml = initial_xml

    # -----------------------------------------------------------
    # 8) 対話ループ
    # -----------------------------------------------------------
    hist_path = os.path.expanduser("~/.im_history")
    session = PromptSession(history=FileHistory(hist_path))

    with patch_stdout(raw=True):  # Gemini のストリーム出力と衝突しない
        while True:
            try:
                user_in = session.prompt("> ", multiline=False).strip()
            except KeyboardInterrupt:
                console.print("\n🌟 Bye!")
                break

            if user_in == "/exit":
                break

            if user_in == "/copy":
                match = re.search(r"<minutes_text>(.*?)</minutes_text>", latest_xml, re.S | re.I)
                clip = match.group(1) if match else latest_xml
                try:
                    pyperclip.copy(clip)
                    console.print("[green]✓ 議事録をクリップボードへコピーしました")
                except pyperclip.PyperclipException:
                    console.print("[yellow]⚠ クリップボードが利用できません")
                continue

            follow = f"<user_followup>{user_in}</user_followup>"
            console.rule("[bold green]Updating minutes")
            resp = stream_request(follow)
            if resp:
                latest_xml = resp


if __name__ == "__main__":
    main()
