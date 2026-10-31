# 今後の方針・実施順序・実際の操作

2026年10月31日。各条件3試行の原本照合後の手順。

## 方針と完成までの流れ

研究の中心は「APK静的情報と通信メタデータを明示ポリシーへ照合し、不明・未指定・未観測を残して証拠へ追跡する支援」とする。基本条件の単純反復は一区切りとし、次は判断可能な範囲と不足情報を比較する。

| 順序 | 作業 | 操作する場所 | 完了の目安 |
|---|---|---|---|
| 1 | 今回9試行と履歴全13試行を保管 | Mac / GPT側 | ZIPと試行台帳が対応し、再提出を重複計数しない。原本照合は実施済み |
| 2 | 同じZIPで3ポリシー×3証拠方式を比較 | Python、Emulator不要 | 1試行9レポート、9試行なら81処理結果。新しい端末試行ではない |
| 3 | 代表例から根拠をたどる | ブラウザ / GPT側 | HTTP整合・禁止候補・未指定、短時間UDPの帰属不明を説明できる |
| 4 | 主張に必要な未確認条件を補う | 手元Emulator | HTTPS正常とHTTP接続失敗の独立根拠。専用手順の整備後に実行 |
| 5 | 関連研究・比較表・考察を仕上げる | GPT側と著者 | 査読論文比較と新規性、限界、結果が対応 |
| 6 | 著者情報・様式を確認して論文を完成 | 著者・指導教員 | 未実施の結果や申告だけの試行を補わず、主張に根拠がある |

文献調査は2～4と並行して進める。UDP保持時間だけの因果を主要な結論にしなければ、同一APKで保持を切り替える追加実験を必須にしない。通信なしの追加反復は同じ結果との報告を保持し、同じ実験のやり直しを一律に求めない。

## いま実行する操作：比較ツールを準備する

配布ファイルは `APK_POLICY_COMPARISON_RUNNER.zip`。これは端末取得用のguided-trial-runnerとは別の、保存済みZIPを解析するツールである。ADB、Emulator、PCAPdroid、参照サーバーの起動は不要。

1. ZIPをダウンロードして展開する。
2. 展開した `apk-policy-comparison` フォルダをMacのDocumentsへ置く。
3. VSCodeで「ファイル → フォルダーを開く」からそのフォルダを開き、ターミナルを開く。
4. 次を実行する。既存システムの仮想環境とは別に作成する。

```bash
cd "$HOME/Documents/apk-policy-comparison"
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps -e .
mkdir -p input
open input
```

Pythonは3.11以上を使用する。実験時のPython 3.11.9を利用できれば、その環境を使う。最初の依存導入はインターネット接続が必要であり、エラーの場合はその後の解析へ進まず表示を確認する。

開いたinputフォルダへ、次の9 ZIPをFinderでコピーする。ZIPは展開せず入れる。元の保存場所の原本は残す。

```text
http-test-001.zip
http-test-002.zip
http-test-003.zip
udp-short-001.zip
udp-short-002.zip
udp-short-003.zip
udp-hold-001.zip
udp-hold-002.zip
udp-hold-003.zip
```

## 最初にHTTPの1試行だけを解析する

```bash
.venv/bin/python tools/compare_guided_trial.py \
  --archive input/http-test-001.zip \
  --out results/http-test-001

open results/http-test-001/index.html
```

完了時に `reports: 9` と出る。HTML一覧から各「根拠付きレポート」を開く。出力済みの場所は上書きしないため、既に実行した場合は `--out results-repeat/http-test-001` のように新しい保存先を使う。

3ポリシーは、取得前に保存されたIP・portの許可条件、そのネットワーク条件だけを変更した事後の禁止条件、事後の未指定条件である。SDK・権限等の他条件は保持する。各ポリシーに静的のみ・動的のみ・統合を適用する。

禁止・未指定は事後の反実仮想であり、元の開発者が取得前にそう宣言したという実験へ変更しない。今回の解析は比較方法の確認・事例分析であり、独立した未知アプリへの精度測定ではない。

## 残りの8試行を解析する

HTTP 001の一覧が開けたら、同じターミナルで次を実行する。HTTP 001は再実行しない。

```bash
for trial_id in http-test-002 http-test-003 udp-short-001 udp-short-002 udp-short-003 udp-hold-001 udp-hold-002 udp-hold-003
do
  .venv/bin/python tools/compare_guided_trial.py \
    --archive "input/${trial_id}.zip" \
    --out "results/${trial_id}" || break
done

open results
```

各試行のindex.htmlで9方式の結果を確認できる。最後まで実行すると、9試行×9処理条件の計81レポートになる。81件の新しい通信実験や独立標本が増えたとは数えない。エラーで止まった試行は結果を確認し、既存の出力を消さずに新しい保存先で再解析する。

出力は次の構成になる。

```text
results/http-test-001/
  index.html
  comparison-summary.csv
  comparison-summary.json
  archive-review.json
  originals/
  base-run/
  policies/
  comparisons/
    captured_allowlist/
      static-only/report.html
      dynamic-only/report.html
      integrated/report.html
    counterfactual_deny_all/
      ...
    counterfactual_unspecified/
      ...
```

各report.htmlは同じフォルダ内のrun.json、findings.json、flows.jsonl、evidence/index.json、raw等と一緒に保存する。HTMLだけを別の場所へ移すと証拠へのリンクが切れる。

## 結果の読み方と確認する操作

最初は次の3例を開く。

```bash
open results/http-test-001/index.html
open results/udp-short-001/index.html
open results/udp-hold-001/index.html
```

| 例 | 見る場所 | 確認すること |
|---|---|---|
| HTTP / 統合 / 許可 | 対象通信の判定 | 記録されたIP・portが許可条件と整合する |
| HTTP / 統合 / 禁止 | 対象通信の判定 | 不一致候補になる。アプリの安全性や漏えいは断定しない |
| HTTP / 統合 / 未指定 | 対象通信の判定 | 要確認になる。未指定を禁止に変えない |
| 短時間UDP / 動的・統合 | 帰属に関する指摘 | 不明のまま保持する。対象通信の判定なしを「通信なし」と読まない |
| 保持UDP / 動的・統合 | 対象通信と帰属 | UID一致に基づいて許可・禁止・未指定を照合できる |
| 静的のみ | 除外範囲・静的指摘 | 動的証拠を除外したことと無通信を区別する。権限・設定を確認する |

根拠付きレポートの指摘にある証拠IDをクリックし、証拠索引から元CSV等を開く。CSVのUID、package、宛先と該当行を確認する。統合方式でも、CSVにないHTTP/TLS成立や本文を自動的に補わない。サーバー記録は保存するが、現行照合器はCSV行と自動結合しない。

`comparison-summary.csv` の unknown件数は、全フローの帰属不明の指摘数であり、対象UDPだけの件数ではない。背景通信が含まれ得るので、対象通信数や帰属精度に読み替えない。取得品質partialも維持する。

## 解析結果をこのチャットへ渡す場合

各試行の `comparison-summary.json` と `comparison-summary.csv` を添付すれば、比較表と論文の考察に反映できる。入力ZIP9件は既に受領しているため、このチャットの継続では同じZIPを再送する必要はない。

フォルダ全体を渡す場合はFinderでresultsを右クリックし「圧縮」を使う。結果フォルダには原本と証拠リンクが含まれるため、GitHubへ公開するのは集計版とする。これは既に保存している研究記録の扱いに合わせるもので、新しい承認手順を追加するものではない。

## 次の追加実験の方針と操作範囲

### HTTPS正常通信

必要な確認は「アプリ側の証明書検証が成功した」「サーバーが対象IDを受信した」「PCAPdroidの接続・帰属を保存した」である。本文の復号は必須にしない。使用する宛先・証明書・アプリ信頼設定を固定してから取得する。

現在配布済みのguided-trial-runnerに `--case https` はないため、そのコマンドは実行しない。GPT側で対応APK・信頼設定・取得前後対照とランナーを準備した後、手元では従来どおりVPN同意、PCAPdroid開始・停止・CSV出力を担当する。証明書検証を無効にした結果を通常のHTTPS成功へ置き換えない。

### HTTP接続失敗

取得系の対照用HTTPサーバーは稼働したままにし、対象アプリだけを未使用ポートへ接続させる。取得前後のhealthは成功、対象は接続エラー、対象要求のサーバー受信はなし、CSVには接続試行があるかを確認する。既存HTTP成功用ランナーにそのまま渡す条件ではないため、専用シナリオの準備後に実行する。

これらを実施する場合、各3回を初期案にして条件・期待値を先に保存する。現在の9件の事後比較と混ぜず別の試行IDを付ける。HTTPSや失敗時の挙動まで論文で主張しない範囲に絞る場合は、未実施を制約として明記する選択もできる。

## 論文を仕上げるときの分担

GPT側では今回の比較集計、図表、判定と証拠のワークスルー、TeX改訂、関連研究の比較案を作る。著者側では意図・正解表と実際の操作を確認し、必要な端末取得、所属様式・著者情報、指導教員との確認を行う。

本文の主な残作業は、既存研究との差を査読論文で示すこと、静的のみ・動的のみ・統合の違いを実際の指摘と根拠で説明すること、結果が言える範囲と限界を整えることである。確認負担の削減、AI生成コードの危険性、SDK一般精度を主張する場合は別の評価が必要になる。

## 今回の補助ツールの確認範囲

クラウドでHTTP・短時間UDP・保持UDPの原本各1件を用いて、合計27処理条件の比較と証拠付きレポート生成を確認した。新しい端末実験は行っていない。Mac上の新規依存導入そのものは未実行である。
