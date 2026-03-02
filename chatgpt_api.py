"""
ChatGPT API連携サンプル
OpenAI APIを使用してChatGPTと対話するプログラム
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()


def initialize_client():
    """
    OpenAIクライアントを初期化
    APIキーは環境変数OPENAI_API_KEYから取得
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "APIキーが設定されていません。\n"
            "環境変数OPENAI_API_KEYを設定するか、\n"
            ".envファイルにOPENAI_API_KEY=your_api_keyを追加してください。"
        )
    
    return OpenAI(api_key=api_key)


def chat_with_gpt(client, messages, model="gpt-3.5-turbo"):
    """
    ChatGPTと対話する関数
    
    Args:
        client: OpenAIクライアントインスタンス
        messages: 会話履歴のリスト
        model: 使用するモデル名（デフォルト: gpt-3.5-turbo）
    
    Returns:
        ChatGPTの応答
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"


def main():
    """
    メイン関数：対話型のChatGPTクライアント
    """
    print("=" * 50)
    print("ChatGPT API連携プログラム")
    print("=" * 50)
    print("終了するには 'exit' または 'quit' と入力してください\n")
    
    # クライアントの初期化
    try:
        client = initialize_client()
    except ValueError as e:
        print(f"エラー: {e}")
        return
    
    # 会話履歴の初期化
    messages = [
        {
            "role": "system",
            "content": "あなたは親切で丁寧なアシスタントです。日本語で回答してください。"
        }
    ]
    
    # 対話ループ
    while True:
        # ユーザー入力の取得
        user_input = input("\nあなた: ").strip()
        
        # 終了条件
        if user_input.lower() in ["exit", "quit", "終了"]:
            print("\n会話を終了します。ありがとうございました！")
            break
        
        if not user_input:
            print("メッセージを入力してください。")
            continue
        
        # ユーザーメッセージを履歴に追加
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        # ChatGPTからの応答を取得
        print("\nChatGPT: ", end="", flush=True)
        response = chat_with_gpt(client, messages)
        print(response)
        
        # アシスタントの応答を履歴に追加
        messages.append({
            "role": "assistant",
            "content": response
        })


def simple_chat_example():
    """
    シンプルな使用例
    """
    try:
        client = initialize_client()
        
        messages = [
            {"role": "system", "content": "あなたは親切なアシスタントです。"},
            {"role": "user", "content": "こんにちは！Pythonについて教えてください。"}
        ]
        
        response = chat_with_gpt(client, messages)
        print("ChatGPTの応答:")
        print(response)
        
    except Exception as e:
        print(f"エラー: {e}")


if __name__ == "__main__":
    # 対話型モードで実行
    main()
    
    # シンプルな例を実行したい場合は、以下のコメントを外してください
    # simple_chat_example()

