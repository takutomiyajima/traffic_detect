# 制御APK 1.1の画面修正

ユーザー提供のAndroid画面で、タイトル・入力欄がシステムバーの下へ入り、操作ボタンの位置をアプリのタイトルバーが覆う状態を確認した。旧版はtargetSdk 35で、タイトルバーとWindowInsetsを明示的に処理していなかった。

修正版はversionCode 2 / versionName 1.1。NoActionBarテーマを指定し、ステータスバー・カメラの切り欠き・ナビゲーションバー・キーボードのInsetsを避ける。内容をスクロール可能にし、操作ボタンを青色の「通信を実行 / Run test」として表示する。待機表示は `waiting — press Run test`。

通信処理・package名は維持し、以前と同じ研究用debug証明書で署名した。旧版の署名と一致することをapksignerで確認したため、`adb install -r` で更新できる。

ビルド・署名・静的検証はクラウドで実行した。端末での修正版の表示とタップ操作は、手元AVDでこれから確認する。端末確認済みと先取りして扱わない。

## 手元Macでの更新

単体の `http-ui-fixed.apk` をDownloadsへ保存した場合:

```bash
adb -s emulator-5554 install -r "$HOME/Downloads/http-ui-fixed.apk"
```

旧試行は画面操作が完了しなかった試行として保存し、次は新しい実験ID `http-003` を使う。サーバの保存先も `handoff/http-003/server-events.jsonl` に切り替える。

サーバ用ターミナルで、旧サーバがあればCtrl+Cで停止してから:

```bash
python -c "import sys; sys.path.insert(0, 'src'); from apk_audit.control_server import main; main()" --log handoff/http-003/server-events.jsonl
```

サーバを動かしたまま、別ターミナルで:

```bash
adb -s emulator-5554 shell am start -S -n org.example.apkaudit.http/.MainActivity --es endpoint http://10.0.2.2:8765/collect --es run_id http-003
adb -s emulator-5554 shell dumpsys package org.example.apkaudit.http > handoff/http-003/package-info.txt
```

青い「通信を実行 / Run test」をタップし、`http_response=200` を確認する。版1.1の表示・操作を先に確認し、正式な取得試行は取得前後の対照・時刻・CSV保存を含めて実施する。

## 研究記録

旧素材は `runs/control-apks-v2`、修正版は `runs/control-apks-v3-ui` に分けて保持する。対応するAPKハッシュはそれぞれのinventory.jsonを使い、別のAPKを同一入力として混ぜない。過去の103項目一致の記録と、修正版の静的確認は別runに保存する。
