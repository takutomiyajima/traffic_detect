# HTTP通信の初回端末観測

2026年10月29日（JST）。実験者のMacとAndroid Emulatorで取得し、このチャットへ渡された原本4点を解析した。クラウドからADBを実行した結果ではない。初回の観測経路確認であり、本評価の精度指標には算入しない。

## 確認結果

| 項目 | 原本から確認した値 |
|---|---|
| 対象package | org.example.apkaudit.http |
| アプリ版 | 1.1（versionCode 2） |
| 対象UID | 10207（appId=10207、User 0 installed=true） |
| 取得ツール版 | PCAPdroid 2.0.2 |
| CSV形式 | 固定ソースで確認した17列のヘッダと一致、データ6行 |
| 対象アプリの接続行 | 1行、TCP、10.0.2.2:8765 |
| 対象行の通信量 | BytesSent=514、BytesRcvd=466、PktsSent=5、PktsRcvd=5 |
| 別UIDの接続行 | 5行、UID 10133、com.google.android.gms |
| サーバー受信 | POST 1件、run_id=ui-check-001、body_bytes=18 |

CSVの対象行はヘッダを1行目とした6行目。FirstSeenは15:15:08.747 JST、LastSeenは15:15:08.751 JST。サーバーログのPOSTは20行目、06:15:09.031456 UTC（15:15:09.031456 JST）。サーバーには別途GET 5件もあるが、対象アプリのPOSTへ合算しない。

CSVはProto=HTTP、Status=Closedと表示している。ただし、これだけでTCP成立、HTTP応答200、本文の意味を証明しない。サーバーの受信ログではPOSTが確認でき、本文ハッシュは制御アプリの `audit=ui-check-001` と一致した。CSVの514/466 bytesは本文18 bytesとは計測対象が異なる。

## 対応付けの限界

packageとUID、既知の宛先、近い時刻に整合性がある。一方、CSVにはrun_idやサーバーのconnection_idがないため、異なる取得元の厳密な同一接続対応は候補として保持する。未補正のサーバー受信時刻とCSV開始時刻の差は0.284456秒である。時計差が未測定であり、この差を通信遅延や時計補正値として扱わない。

フォルダ名がhttp-003であっても、今回のPOSTに記録された実験IDはui-check-001である。原本を書き換えてhttp-003へ合わせない。

取得開始・終了時刻、前後対照の実施記録、アプリ画面・logcat、操作時刻、API・ABI・AVDイメージ、端末上のAPKハッシュは未提出。以前のGETは今回のCSVに含まれる取得前後対照と確認できない。Google Play開発者サービスの背景通信は、独立して操作した別アプリ対照とは区別する。

そのため、時計差を0と仮定した正式importや静的・動的・統合の精度集計は行わず、不明項目を残した個別集計に留めた。

## 原本と再解析

原本は `runs/received-http-ui-check-001/raw/` に複製し、変更せず保存した。個別パッケージ情報の原文はこの公開用要約に含めない。SHA-256:

| ファイル | SHA-256 |
|---|---|
| capture.csv | fc90c2835d2ae51fad9a5e406a1726556517bd2f343d9aba416414fc771c86d3 |
| server-events.jsonl | 3f2f3b7aec2a8f9ec624da9ecb11cef47c71ee07782e706f031969fb9b1e0b32 |
| app-package.txt | da3d4a64c9a19038eda9b2fae3b814a0db126b2dd553b155364a0648ef2e78dc |
| pcapdroid-package.txt | e11f773ef6fe376908e619b9dd2f9921ea7ed300c4f6e8cd6cf257fe45066fb6 |

ローカル原本がある環境で次により再解析できる。

```bash
PYTHONPATH=src .venv/bin/python runs/received-http-ui-check-001/analyze.py
```

`analysis.json` に各行、原本ハッシュ、未測定項目、照合候補を保存する。解析スクリプトは、ヘッダ、数値、時刻順序、インストールUID、サーバー本文ハッシュを検査する。これは一般の帰属精度を検証する独立した正解ラベルではない。

## 次の1試行で残すもの

新しい実験IDと保存先を一致させ、取得前後対照、PCAPdroid取得の開始・停止、アプリ操作時刻、画面とlogcat、AVD情報、時計比較を記録する。条件を確認した後にHTTP反復、通信なし、UDP、別アプリ同時通信等へ進む。過去の未記録時刻を推測して補わない。
