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
