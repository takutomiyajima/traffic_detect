# UDPアプリ識別の切り分け用ランナー

現時点の根拠: udp-auto-001ではサーバー受信とUDP CSV行を確認したが、CSVのUIDは-1、PackageNameはunknown。実験者から手動操作でも同様だったと報告された。絞り込み後もアプリ名がUnknownとの追加報告があるが、そのCSVのUID・packageは確認待ち。

まずCSVのUIDを確認する。UIDが対象の値でアプリ名だけ不明なら表示名・packageの解決を調べる。UIDも-1ならOSによる通信元照会が不成立である。フィルター選択だけを正解ラベルにせず、送信元の確定とは区別する。

## 保持時間を変える追加条件

このZIPは、UDPソケットを送信後2秒間開いたまま保持する診断版を含む。旧版と同じpackage org.example.apkaudit.udp、同じ署名、宛先・本文・未接続UDP方式で、保持待機とそのログを追加した。版は1.2、versionCode 3。UIDが取得できるようになることは未検証。元の失敗を置き換える成功版とは呼ばず、追加条件として扱う。

APK SHA-256: `1236cb4fe9d3034c6bd5f5726d9402f0ab2f80ca9c30114c27d59fd54d3ec9d7`。

1. ZIPを展開し、`guided-trial-runner-udp-hold` をDocumentsへ置く。既存フォルダと試行は残す。
2. この新しいフォルダをVSCodeで開く。
3. 必要な場合の追加診断は次を実行する。

```bash
python run_guided_trial.py --case udp_hold --trial-id udp-hold-001
```

PCAPdroidは前後対照を確認できるよう全アプリ、VPN方式、TLS復号なしで新たに開始し、案内に従いstartと入力する。自動操作が終わって停止の案内が出たらPCAPdroidを止めてstopと入力する。状態を回答し、CSVを `capture-udp-hold-001.csv` としてDownloadへ保存し、保存先の確認でEnterを押す。

終了後:

```bash
open handoff
```

`udp-hold-001.zip` を渡す。元のudp-auto-001とは別条件で保存する。UDP表示だけでUIDを補完せず、不明は不明として保持する。

この実行は同じpackageの新版をinstall -rで更新する。既存のUDP版1.1への通常の戻しインストールはdowngradeとして拒否され得るため、以後の追加診断はudp_holdを指定する。アンインストールによるUID変更を避け、戻し方が必要な場合は別途条件を確認する。

ホスト側全テスト88件成功。保持版APKはビルド・署名・静的解析を確認済み。実AndroidのUID帰属改善は未実証で、端末の初回結果で評価する。Chrome表示の自動読取りができない場合だけ、従来同様ok:trueの目視確認を求める。
