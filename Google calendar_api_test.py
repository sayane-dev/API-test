"""
Googleカレンダーにサービスアカウントで予定を追加するサンプル
"""

import os
from datetime import datetime, timedelta

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# スコープ: カレンダーの読み書き
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# スプレッドシート連携と同じ credentials.json（サービスアカウントのJSONキー）を使用
# 環境変数 GOOGLE_APPLICATION_CREDENTIALS 未設定時は、このスクリプトと同じフォルダの credentials.json
_default_creds = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.json")
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", _default_creds)


def get_calendar_service():
    """サービスアカウントでCalendar APIのクライアントを取得"""
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    return build("calendar", "v3", credentials=creds)


def create_event(
    calendar_id: str,
    summary: str,
    start_datetime: datetime,
    end_datetime: datetime,
    *,
    description: str | None = None,
    location: str | None = None,
    timezone: str = "Asia/Tokyo",
) -> dict:
    """
    カレンダーに予定を追加する

    Args:
        calendar_id: カレンダーID（"primary" = サービスアカウントの主カレンダー。
                     共有されたカレンダーを使う場合はそのカレンダーIDを指定）
        summary: 予定のタイトル
        start_datetime: 開始日時
        end_datetime: 終了日時
        description: 説明（任意）
        location: 場所（任意）
        timezone: タイムゾーン（デフォルト: Asia/Tokyo）

    Returns:
        作成されたイベントのAPIレスポンス

    注意:
        サービスアカウントで「他人の」カレンダーに予定を入れる場合は、
        Googleカレンダーでそのカレンダーをサービスアカウントのメールアドレスと共有してください。
    """
    # RFC3339形式に変換（Calendar APIは dateTime + timeZone を推奨）
    start_rfc = start_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    end_rfc = end_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    body = {
        "summary": summary,
        "start": {"dateTime": start_rfc, "timeZone": timezone},
        "end": {"dateTime": end_rfc, "timeZone": timezone},
    }
    if description is not None:
        body["description"] = description
    if location is not None:
        body["location"] = location

    service = get_calendar_service()
    event = (
        service.events()
        .insert(calendarId=calendar_id, body=body)
        .execute()
    )
    return event


def create_all_day_event(
    calendar_id: str,
    summary: str,
    start_date: datetime,
    end_date: datetime | None = None,
    *,
    description: str | None = None,
    location: str | None = None,
) -> dict:
    """
    終日予定を追加する（日付のみ、時刻なし）

    Args:
        calendar_id: カレンダーID
        summary: 予定のタイトル
        start_date: 開始日（時刻は無視され、その日の0:00として扱う）
        end_date: 終了日。省略時は start_date と同じ日（1日だけの終日予定）
        description: 説明（任意）
        location: 場所（任意）

    Returns:
        作成されたイベントのAPIレスポンス
    """
    if end_date is None:
        end_date = start_date
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    body = {
        "summary": summary,
        "start": {"date": start_str},
        "end": {"date": end_str},
    }
    if description is not None:
        body["description"] = description
    if location is not None:
        body["location"] = location

    service = get_calendar_service()
    event = (
        service.events()
        .insert(calendarId=calendar_id, body=body)
        .execute()
    )
    return event


def add_event_from_input(calendar_id: str, default_duration_minutes: int = 60) -> dict | None:
    """
    ユーザー入力（日付・時刻・タイトル）から予定をカレンダーに追加する。
    時刻を空欄にした場合は終日予定として追加する。

    Args:
        calendar_id: カレンダーID
        default_duration_minutes: 時間指定時の予定の長さ（分）。デフォルト60分。

    Returns:
        作成されたイベントのAPIレスポンス。失敗時は None。
    """
    print("予定を追加します。以下を入力してください。\n")
    date_str = input("日付（例: 2025-03-15）: ").strip()
    time_str = input("時刻（例: 14:30、終日の場合は空欄）: ").strip()
    title = input("タイトル: ").strip()

    if not title:
        print("エラー: タイトルを入力してください。")
        return None

    try:
        start_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("エラー: 日付は YYYY-MM-DD 形式で入力してください。")
        return None

    # 時刻が空欄 → 終日予定
    if not time_str:
        return create_all_day_event(
            calendar_id,
            summary=title,
            start_date=start_date,
        )
    # 時刻あり → 時間指定の予定
    try:
        start_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        end_dt = start_dt + timedelta(minutes=default_duration_minutes)
    except ValueError:
        print("エラー: 時刻は HH:MM 形式で入力してください。")
        return None

    return create_event(
        calendar_id,
        summary=title,
        start_datetime=start_dt,
        end_datetime=end_dt,
    )


if __name__ == "__main__":
    # 使用例: カレンダーIDは "primary"（サービスアカウントの主カレンダー）
    # または、共有されたカレンダーのID（設定 → カレンダーの統合 → カレンダーID）
    CALENDAR_ID = "kh.sy.rbaih@gmail.com"

    try:
        # 入力された日付・時刻・タイトルで予定を追加
        event = add_event_from_input(CALENDAR_ID)
        if event:
            print("\n予定を追加しました。")
            print("  イベントID:", event.get("id"))
            print("  リンク:", event.get("htmlLink"))

        # 従来の固定予定で試す場合は以下を有効に
        # now = datetime.now()
        # start = now + timedelta(hours=1)
        # end = start + timedelta(hours=1)
        # event = create_event(
        #     CALENDAR_ID,
        #     summary="APIテスト予定",
        #     start_datetime=start,
        #     end_datetime=end,
        #     description="Google Calendar API からの作成テスト",
        #     location="オンライン",
        # )
        # print("予定を追加しました（時刻指定）")
        # print("  イベントID:", event.get("id"))
        # print("  リンク:", event.get("htmlLink"))

    except FileNotFoundError:
        print(
            "エラー: 認証ファイルが見つかりません。\n"
            "1. Google Cloud Consoleでサービスアカウントを作成\n"
            "2. Calendar API を有効化\n"
            "3. JSONキーをダウンロードし、credentials.json としてこのフォルダに保存\n"
            "4. 予定を入れたいカレンダーをサービスアカウントのメールアドレスと共有"
        )
    except Exception as e:
        print("エラー:", e)
