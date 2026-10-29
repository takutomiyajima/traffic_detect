# 次のHTTP試行: http-004

現在使っているMacのプロジェクトフォルダで行う。http-004を既に使っている場合は全箇所を次の未使用IDに変える。旧試行は削除しない。時計ツールは手元に取得済みの `handoff/clock-check-001/measure_android_clock.py` を使う。今回も観測系の受入確認であり、未知アプリへの精度評価ではない。

## 1. ターミナルA: サーバー

以前自分が起動したサーバーが動いている場合は、そのターミナルでCtrl+Cで停止する。次を起動し、listeningが出たまま動かしておく。

```bash
python -c "import sys; sys.path.insert(0, 'src'); from apk_audit.control_server import main; main()" --log handoff/http-004/server-events.jsonl
```

## 2. ターミナルB: 今回の状態と時計差

サーバーが作ったフォルダを保存先に使う。以前のUIDや時計差を今回の値として流用しない。

```bash
adb -s emulator-5554 shell dumpsys package org.example.apkaudit.http > handoff/http-004/app-package.txt
adb -s emulator-5554 shell dumpsys package com.emanuelef.remote_capture > handoff/http-004/pcapdroid-package.txt
adb -s emulator-5554 shell settings get global http_proxy > handoff/http-004/http-proxy.txt
adb -s emulator-5554 shell pm path org.example.apkaudit.http > handoff/http-004/installed-apk-path.txt
python handoff/clock-check-001/measure_android_clock.py --serial emulator-5554 --out handoff/http-004/clock-before.json
```

proxyが以前の `10.0.2.2:8082` へ戻っていないことを確認する。時計測定がunknownのときもJSONを残す。正式な時刻対応の成功とせず、原因を確認する。installed-apk-pathはハッシュではない。APK原本の照合に必要になった場合はそのパスから取り出してハッシュを追加確認する。

## 3. ターミナルC: 継続logcat

VSCodeの「+」で3つ目のターミナルを開き、同じプロジェクトフォルダから実行する。

```bash
adb -s emulator-5554 logcat -v epoch -T 1 ApkAuditControl:I AndroidRuntime:E "*:S" > handoff/http-004/app-logcat.txt
```

画面に出力がなくても記録中である。最後の停止手順まで動かしておく。過去のバッファは消さない。含まれた旧ログはrun=http-004等で分ける。

## 4. PCAPdroidで取得開始と前対照

VPN方式、全アプリ、TLS復号なしの設定で取得する。開始ボタンを押す直前と直後にターミナルBでそれぞれ時刻を保存する。これは正確な開始時刻ではなく、操作を挟んだ境界を記録する。

直前:

```bash
date -u '+%Y-%m-%dT%H:%M:%SZ' > handoff/http-004/capture-start-earliest.txt
```

取得開始直後:

```bash
date -u '+%Y-%m-%dT%H:%M:%SZ' > handoff/http-004/capture-start-latest.txt
adb -s emulator-5554 shell am start -W -a android.intent.action.VIEW -d 'http://10.0.2.2:8765/health?check=http-004-before' -p com.android.chrome
```

ChromeにJSONのok:trueが表示されるか確認し、表示のスクリーンショットを保存する。

```bash
adb -s emulator-5554 exec-out screencap -p > handoff/http-004/health-before.png
```

前対照が失敗した場合は結果を残し、成功試行として扱わない。

## 5. 対象アプリの1回操作

ターミナルB:

```bash
adb -s emulator-5554 shell am start -S -n org.example.apkaudit.http/.MainActivity --es endpoint http://10.0.2.2:8765/collect --es run_id http-004
```

Run testを1回だけ押す。action_startedと応答はアプリのlogcatに端末時刻で記録される。HTTP応答の表示結果をそのまま保存する。

```bash
adb -s emulator-5554 exec-out screencap -p > handoff/http-004/app-result.png
```

Runから30秒観測する。前後対照や反復を含めたこの窓を、他の未実行ケースへ一般化しない。エラーでも再タップせず記録する。

## 6. 後対照、取得停止、後の時計差

```bash
adb -s emulator-5554 shell am start -W -a android.intent.action.VIEW -d 'http://10.0.2.2:8765/health?check=http-004-after' -p com.android.chrome
```

再びok:trueを確認し、画像を保存する。

```bash
adb -s emulator-5554 exec-out screencap -p > handoff/http-004/health-after.png
date -u '+%Y-%m-%dT%H:%M:%SZ' > handoff/http-004/capture-stop-earliest.txt
```

PCAPdroidで取得停止を押す。その直後に:

```bash
date -u '+%Y-%m-%dT%H:%M:%SZ' > handoff/http-004/capture-stop-latest.txt
python handoff/clock-check-001/measure_android_clock.py --serial emulator-5554 --out handoff/http-004/clock-after.json
```

前後時計差が変わっている場合は原サンプルと共に評価する。別バッチの中点を単純平均してε=0としない。キャプチャ全体の補正と操作区間の境界判定はGPT側で条件を検討する。

## 7. 書出しと引渡し

PCAPdroidの全接続CSVをDownloadへcapture-http-004.csvとして保存した場合:

```bash
adb -s emulator-5554 pull /sdcard/Download/capture-http-004.csv handoff/http-004/capture.csv
```

実際の名前が違う場合はコピー元だけを合わせる。保存場所が不明なら:

```bash
adb -s emulator-5554 shell 'find /sdcard/ -type f -iname "*.csv" 2>/dev/null'
```

ターミナルCをCtrl+Cで停止し、その後ターミナルAもCtrl+Cで停止する。Bでフォルダを開く。

```bash
open handoff/http-004
```

フォルダ一式をFinderで圧縮してチャットへ添付する。PCAPdroid開始/停止の失敗、対照表示、Run回数、設定変更があればテキストで併記する。host日時の秒単位の記録と人の画面操作は誤差を含み、厳密なUIイベント区間と同一視しない。

受領後に原本hash、前後の時計、UID、アプリaction_started、CSVの対象接続、サーバのrun_idを照合する。不足条件を推測でpassedにしない。サーバのGETと対象アプリのPOST、HTTP要求数とTCP接続数は別に数える。
