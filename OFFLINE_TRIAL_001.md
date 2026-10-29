# 通信なし対照: offline-001

HTTPの陽性対照に続き、通信を行わない自作APKを同じAVDで観測する。対象は `org.example.apkaudit.offline` 版1.1、APK SHA-256は `39dd104a69408f8f49a60934388933c2dd2cf855c1abed2faf0f3147d75f6280`。期待結果はローカル処理の完了と、指定窓で対象通信を観測しないこと。全機能・全条件で通信が存在しないという結論にはしない。

取得前のポリシーは配布の `OFFLINE_001_POLICY.json`（システム内は `examples/handoff/offline-001.intent.json`）として固定した。通信と権限宣言は禁止、SDK条件は未指定。開発確認用の自作素材であり、未知アプリの精度評価とは分ける。

`offline-control.apk` をMacのDownloadsへ保存する。この手順中はHTTPアプリのRunを押さない。全コマンドをMacのプロジェクトフォルダから実行する。IDを既に使った場合は全箇所を次の未使用IDに変更し、古い記録は残す。

## 1. ターミナルA: サーバーを起動

以前のサーバーをそのターミナルでCtrl+Cで停止してから:

```bash
python -c "import sys; sys.path.insert(0, 'src'); from apk_audit.control_server import main; main()" --log handoff/offline-001/server-events.jsonl
```

listeningが出たままにする。今回は前後のブラウザ対照に使用する。

## 2. ターミナルB: インストールと記録

```bash
adb -s emulator-5554 install -r "$HOME/Downloads/offline-control.apk"
adb -s emulator-5554 shell dumpsys package org.example.apkaudit.offline > handoff/offline-001/app-package.txt
adb -s emulator-5554 shell dumpsys package com.emanuelef.remote_capture > handoff/offline-001/pcapdroid-package.txt
adb -s emulator-5554 shell 'for p in $(pm path org.example.apkaudit.offline); do toybox sha256sum "${p#package:}"; done' > handoff/offline-001/installed-apk-sha256.txt
adb -s emulator-5554 shell settings get global http_proxy > handoff/offline-001/http-proxy.txt
python handoff/clock-check-001/measure_android_clock.py --serial emulator-5554 --out handoff/offline-001/clock-before.json
```

installのSuccessを確認する。失敗や時計unknownはそのまま残し、成功と扱わない。

## 3. ターミナルC: logcatを継続保存

```bash
adb -s emulator-5554 logcat -v epoch -T 1 ApkAuditControl:I AndroidRuntime:E "*:S" > handoff/offline-001/app-logcat.txt
```

表示がなくても記録中。最後まで止めない。

## 4. 取得開始と前対照

PCAPdroidは全アプリ・VPN方式・TLS復号なしとする。Bで開始直前の時刻を保存する。

```bash
date -u '+%Y-%m-%dT%H:%M:%SZ' > handoff/offline-001/capture-start-earliest.txt
```

PCAPdroidで取得開始を押してから:

```bash
date -u '+%Y-%m-%dT%H:%M:%SZ' > handoff/offline-001/capture-start-latest.txt
adb -s emulator-5554 shell am start -W -a android.intent.action.VIEW -d 'http://10.0.2.2:8765/health?check=offline-001-before' -p com.android.chrome
```

Chromeでok:trueを確認して:

```bash
adb -s emulator-5554 exec-out screencap -p > handoff/offline-001/health-before.png
```

## 5. 対象アプリを1回操作

```bash
adb -s emulator-5554 shell am start -S -n org.example.apkaudit.offline/.MainActivity --es run_id offline-001
```

通信先の入力は不要。Run testを1回押し、表示された結果を保存する。期待表示は `local_only_completed`。

```bash
adb -s emulator-5554 exec-out screencap -p > handoff/offline-001/app-result.png
sleep 30
```

30秒が終わりターミナルのプロンプトが戻ってから次へ進む。

## 6. 後対照と取得停止

```bash
adb -s emulator-5554 shell am start -W -a android.intent.action.VIEW -d 'http://10.0.2.2:8765/health?check=offline-001-after' -p com.android.chrome
```

ok:trueを確認して:

```bash
adb -s emulator-5554 exec-out screencap -p > handoff/offline-001/health-after.png
date -u '+%Y-%m-%dT%H:%M:%SZ' > handoff/offline-001/capture-stop-earliest.txt
```

PCAPdroidで取得停止を押してから:

```bash
date -u '+%Y-%m-%dT%H:%M:%SZ' > handoff/offline-001/capture-stop-latest.txt
python handoff/clock-check-001/measure_android_clock.py --serial emulator-5554 --out handoff/offline-001/clock-after.json
```

## 7. 書出しと引渡し

CSVをDownloadへ `capture-offline-001.csv` としてエクスポートした場合:

```bash
adb -s emulator-5554 pull /sdcard/Download/capture-offline-001.csv handoff/offline-001/capture.csv
```

名前が違う場合はコピー元だけを変更する。探す場合:

```bash
adb -s emulator-5554 shell 'find /sdcard/ -type f -iname "*.csv" 2>/dev/null'
```

操作中にPCAPdroidの停止・一時停止・エラーがあったか、Runの回数、実際の設定変更を短いメモにして同じフォルダへ保存する。見ていなかった区間は不明と書き、欠落なしと推測しない。

ターミナルC、AをそれぞれCtrl+Cで停止し、Bでフォルダを開く。

```bash
open handoff/offline-001
```

フォルダ一式をFinderで圧縮してチャットへ添付する。背景のGoogle/Chrome等の行があっても、それだけで対象アプリの通信とは扱わない。対象行がゼロでも、取得系や操作の条件が不明なら「通信なし」と確定せず判定不能として残す。
