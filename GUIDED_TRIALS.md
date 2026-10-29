# PCAPdroidの操作を手動にする半自動実験

対象は現在のAPI 35 Emulator（emulator-5554）、PCAPdroid 2.0.2、Chrome、配布したHTTP・通信なし・UDPの自作APK。Python 3.11以上とADBを使う。pipでの追加インストール、Gradle、root権限は不要。

## 導入

1. 配布する `guided-trial-runner.zip` をMacへ保存し、Finderで展開する。
2. 展開した `guided-trial-runner` フォルダをVSCodeで開く。中に `run_guided_trial.py`、`measure_android_clock.py`、`apk_audit/`、`apks/` がある。
3. エミュレータを起動してロックを解除する。以前のPythonサーバーとlogcatが動いていれば、それぞれのターミナルでCtrl+Cで停止する。ランナーが自分のサーバーとlogcatを起動する。
4. このフォルダのターミナルで次を実行する。

```bash
python run_guided_trial.py --case offline --check
```

`ready: true` が出れば環境とAPKの事前チェックは通過。これは端末での全操作やPCAPdroidの取得を検証したという意味ではない。既存サーバーのポート使用も本実行で確認する。エラーなら出力をそのままチャットへ渡す。

## 最初の1試行

```bash
python run_guided_trial.py --case offline --trial-id offline-auto-001
```

同じIDの保存先は上書きしない。既に使っている場合は `offline-auto-002` などに変える。

ランナーの案内に従う。

1. **開始**: エミュレータでPCAPdroidを開き、全アプリ・VPN方式・TLS復号なしを確認して記録開始。VPN許可が出たら対応し、記録中になったことを確認してからターミナルへ戻り `start` と入力する。
2. **自動操作**: ブラウザの前対照、対象アプリの起動、Runボタン1回、応答確認・画像保存、30秒の待機、後対照が自動で進む。アプリのRunを手動で押さない。画面が切り替わる間も追加操作はしない。
3. **停止**: 案内が出たらPCAPdroidで停止し、ターミナルで `stop` と入力する。停止案内まで待つ。
4. **取得状態**: 記録中の停止・一時停止・エラーがなかったと確認できるなら `none`、あれば `problem`、確認できなければ `unknown` と入力する。これは実験者の申告として保存する。
5. **CSV保存**: PCAPdroidで全接続のCSVをDownloadへ `capture-offline-auto-001.csv` として保存する。ターミナルの保存先確認でEnterを押すと、そのファイルを回収する。違う名前なら `/sdcard/Download/実際の名前.csv` を入力する。`list` でCSV一覧を表示できる。

ChromeのJSON応答をUIから自動読取りできない場合に限り、人に `ok:true` の表示確認を求める。確認できた場合だけ `ok` と入力する。その対照は自動検証とは分けて記録する。

## 結果を渡す

終了時にZIPのパスとstatusを表示する。正常に記録を集めた場合は `status: collected`。`quality: partial` は時計モデルや取得の独立確認に限界を残す印であり、通信の失敗と同じ意味ではない。`collected_needs_review` や `failed` の場合も原記録は残る。

```bash
open handoff
```

`offline-auto-001.zip` をチャットへ添付する。サーバー・logcatはランナーが自分で起動したものを終了する。詳細な静的解析・3方式比較・図表・論文への反映は、受領後こちらで実行する。Mac側ランナーの集計は取得状況の基本チェックである。

## HTTP・UDPへ進む場合

```bash
python run_guided_trial.py --case http --trial-id http-auto-001
```

```bash
python run_guided_trial.py --case udp --trial-id udp-auto-001
```

各試行でPCAPdroidを新たに開始・停止し、CSVを別名で保存する。期待表示はHTTPが `http_response=200`、UDPが `udp_sent`、通信なしが `local_only_completed`。HTTPS、Home後、位置情報等はこのランナーの対象へまだ追加していない。

## 自動で保存する記録

APK原本と取得前の端末APKハッシュ、UID・package・ツール版・環境、取得前ポリシーとハッシュ、前後時計差、継続logcat、サーバー受信、UI XMLと画面、操作・待機時刻、CSV、基本集計、全ファイルのハッシュ一覧。

CSVの古い取り違え、対象UID/packageの矛盾、想定するサーバー受信の不足などは要確認として残す。前後対照のCSV対応は時計モデルに基づく候補であり、CSVとサーバーの厳密な同一接続IDを得たことにはしない。通信なしも指定条件・指定窓の未観測として扱い、全経路での不存在や安全性を保証しない。

## 中断・失敗

`q` またはCtrl+Cで中止できる。ボタンを自動再試行せず、失敗や中断もZIPへ保存する。PCAPdroidはランナーから自動停止しない。中断時はエミュレータを確認し、記録中なら手動で停止する。原因を修正して再試行するときは新しいIDを使う。

## 開発側確認と初回端末確認

全自動テスト87件が成功。そのうち11件が本ランナーのホスト側テストで、ADB/UIを模擬し、実際のローカルHTTP/UDP参照サーバーと組み合わせている。3ケースの記録、ZIPハッシュ、対象行不足、古いCSV、操作の不確実な失敗、中断、既存データ保護等を確認した。

Mac/Emulatorの実UIをこのクラウドで実行したわけではない。最初に1試行を渡してもらい、UI自動操作・保存されたCSV・時刻・ログを確認してから反復へ進む。
