"""
Googleスプレッドシートにサービスアカウントでデータを送信するサンプル
"""

import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# スコープ: スプレッドシートの読み書き
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# 環境変数で認証情報JSONのパスを指定可能（未設定の場合はこのスクリプトと同じフォルダの credentials.json）
_default_creds = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.json")
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", _default_creds)


def get_sheets_service():
    """サービスアカウントでSheets APIのクライアントを取得"""
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)


def append_rows(spreadsheet_id: str, sheet_name: str, values: list[list]) -> dict:
    """
    スプレッドシートの指定シートに行を追加する

    Args:
        spreadsheet_id: スプレッドシートのID（URLの /d/ と /edit の間の文字列）
        sheet_name: シート名（例: "シート1"）
        values: 追加するデータ（2次元リスト。1行 = 1リスト）

    Returns:
        APIのレスポンス
    """
    service = get_sheets_service()
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=f"'{sheet_name}'!A1",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body,
        )
        .execute()
    )
    return result


def update_range(
    spreadsheet_id: str, sheet_name: str, range_a1: str, values: list[list]
) -> dict:
    """
    指定範囲を上書きする

    Args:
        spreadsheet_id: スプレッドシートID
        sheet_name: シート名
        range_a1: A1記法の範囲（例: "A1:C3"）
        values: 書き込む2次元データ
    """
    service = get_sheets_service()
    body = {"values": values}
    full_range = f"'{sheet_name}'!{range_a1}"
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=full_range,
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute()
    )
    return result


if __name__ == "__main__":
    # 使用例
    SPREADSHEET_ID = "1_4PXxZq9xlL6I8Y_QMbfWrZLTQUw0erQflcJJMgauqg"  # 実際のスプレッドシートIDに置き換え
    SHEET_NAME = "シート1"

    # 例: ヘッダー + データを追加
    data = [
        ["名前", "点数", "日付"],
        ["田中", 85, "2025-03-02"],
        ["佐藤", 92, "2025-03-02"],
    ]

    try:
        result = append_rows(SPREADSHEET_ID, SHEET_NAME, data)
        print("追加成功:", result.get("updates", {}).get("updatedRows"), "行")
    except FileNotFoundError:
        print(
            "エラー: 認証ファイルが見つかりません。\n"
            "1. Google Cloud Consoleでサービスアカウントを作成\n"
            "2. JSONキーをダウンロードし、credentials.json として保存\n"
            "3. スプレッドシートをサービスアカウントのメールアドレスと共有"
        )
    except Exception as e:
        print("エラー:", e)
