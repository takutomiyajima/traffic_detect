# APK監査システム — ダウンロード

## 制御APKの画面修正版 1.1

[HTTP制御APKをダウンロード](http-ui-fixed.apk?raw=true)

旧版でタイトルバーに隠れていた操作ボタンを表示するため、NoActionBarと画面Insetsを明示しました。
ボタンの表記は「通信を実行 / Run test」です。
ビルド・署名・静的103項目を確認しました。修正版の端末画面は利用者側で確認してください。

```bash
adb -s emulator-5554 install -r "$HOME/Downloads/http-ui-fixed.apk"
```

[修正内容と再開手順](UI_FIX.md)

## システム・資料・評価素材一式

[更新済みZIPをダウンロード](apk-audit-research-progress.zip?raw=true)

ZIPを展開するとtraffic_detectフォルダが作成されます。
画面修正版はruns/control-apks-v3-ui、旧素材はruns/control-apks-v2です。
旧素材の検証記録は維持しています。論文PDFの実測は修正前の検証で、今回の画面修正とは別です。

- APK SHA-256: `7c7f24e82c80fb1e51df96923dda326571d3c706d496e03efb6373647df01382`
- ZIP SHA-256: `3d87aa7aa99bf53688a21d17dc461b596a8561e18ae12e82ab33ac1e86ed2481`
- Android上の通信取得・UID帰属の全受入試験や未知アプリの精度評価は未完了です。


## 2026-10-29 HTTP初回観測の追記

- [今回の観測結果](http-pilot-report.md)
- [更新した卒論用PDF](thesis-http-pilot.pdf)
- [TeXとシステムを含むZIP](apk-audit-research-progress.zip)

HTTP対照アプリのUIDに一致するCSV行1件と、参照サーバのPOST受信を確認しました。時計差・取得区間・前後対照が未確認の初回観測として記載し、本評価の精度指標には算入していません。今回添付された原本ログとpackage情報の全文は公開成果物に追加していません。


## 時計差測定と修正計画

- [時計差測定の単独Pythonファイル](measure_android_clock.py)
- [測定手順と制約](CLOCK_MEASUREMENT.md)
- [論文修正計画](REVISION_PLAN.md)

測定ツールは標準ライブラリのみで動作し、端末時計・ネットワーク設定を変更しません。開発側の5件のテストと失敗時のCLI動作を確認済みです。実Emulatorの時計測定はこれから行います。


## Next HTTP trial

[http-004 procedure](HTTP_TRIAL_004.md): before/after clock samples, continuous logcat, browser controls, PCAPdroid export, and screenshots.


## http-004の解析結果（2026-10-29）

- [結果と実際の操作条件](HTTP_004_RESULTS.md)
- [更新した卒論用PDF・18ページ](thesis-http-004.pdf)
- [TeX・システム・記録した解析手順のZIP](apk-audit-research-progress.zip)

対象アプリの200応答、UID一致の通信行、サーバPOST、前後のブラウザ対照と時計測定を確認しました。約14秒後の後対照は実験者の実際の操作条件として記録しました。インストールAPKのハッシュ未取得等の残る条件も明記しています。添付ZIPの原本ログ・画面・package情報の全文は公開成果物へ追加していません。
