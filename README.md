# API連携(chatGPT/Google spreadsheet/Google calendar)

上記３つをPythonでAPI連携しました。

## 機能
- chatGPT＝Pythonからプロンプト送信〜会話形式のメッセージ送信対応
- Google spreadsheet＝JSON鍵を用いた安全なAPI接続〜指定シートへのデータ追記
- Google calendar＝Pythonから予定（イベント）作成〜日時指定による自動スケジュール登録
  
## 実行画面
【chatGPT】
<img width="1454" height="854" alt="4-2-1_error解消(GPT)" src="https://github.com/user-attachments/assets/4db20fbc-fc8c-419b-b8f1-220aa866ec00" />

【Google spreadsheet】
<img width="1457" height="862" alt="4-2-1_ｽﾌﾟﾚｯﾄﾞｼｰﾄ連携1" src="https://github.com/user-attachments/assets/62a8c8db-e6f1-4e19-80e3-3f066224d18b" />

【Google calendar】
<img width="1469" height="861" alt="4-2-1ｶﾚﾝﾀﾞｰ連携1" src="https://github.com/user-attachments/assets/fbe27ffe-c81e-4161-a5c1-f4ea9cac3737" />


## エラー解消
【chatGPT】原因：クレジットが切れていて回答が得られなかった
<img width="1454" height="854" alt="4-2-1_error解消(GPT)" src="https://github.com/user-attachments/assets/eeda620d-1d86-437b-b739-5faf0af2774e" />

【Google spreadsheet】原因：JSONのファイルデータ名が生成されたコードと表記が異なっていた
<img width="1470" height="867" alt="4-2-1_error解消" src="https://github.com/user-attachments/assets/4b0c5273-99a9-4c3b-97a6-7a45f4f74352" />

