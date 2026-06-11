# self-care-journal

このリポジトリでは、印刷用PDF `SelfCareJournal_print_final.pdf.pdf` を元に、ローカルPC上で記入できるデジタル版PDF `SelfCareJournal_fillable.pdf` を生成します。

Codex上で完成PDF本体を返す運用ではなく、GitHubには **PDF作成スクリプトと手順書だけ** を残す方針です。完成PDFは各自のPC上で生成してください。

## できること

`create_fillable_journal_pdf.py` は、元PDFのページ内容を画像化せず、既存ページの上に透明なPDFフォームとリンク注釈だけを追加します。

- 元PDFの見た目を変えません。
- ページをJPEG化しません。
- ページ内容を再圧縮しません。
- 元PDFを背景として保持します。
- 透明フォームだけを重ねます。
- P3のチェックボックスをクリック可能にします。
- P5の記入欄を入力可能にします。
- P7のチェックボックスをクリック可能にします。
- P7の「その他」欄と下部記入欄を入力可能にします。
- P9の Blog / note / X をクリック可能リンクにします。
- iPhoneの「ファイル」アプリでチェックと入力ができるAcroForm形式で出力します。

## 必要なもの

- Python 3.10以上
- 入力PDF: `SelfCareJournal_print_final.pdf.pdf`
- Pythonライブラリ: `pypdf`

ライブラリは `requirements.txt` にまとめています。

## Windowsでの実行手順

### 1. Pythonを確認する

PowerShellを開いて、次を実行します。

```powershell
py --version
```

Pythonのバージョンが表示されればOKです。表示されない場合は、Microsoft StoreまたはPython公式サイトからPython 3をインストールしてください。

### 2. このフォルダへ移動する

例：デスクトップにこのリポジトリを置いた場合。

```powershell
cd "$env:USERPROFILE\Desktop\self-care-journal"
```

### 3. 必要なライブラリを入れる

```powershell
py -m pip install -r requirements.txt
```

もし `pip` が古いと言われる場合は、先に次を実行してから再度インストールしてください。

```powershell
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

### 4. PDFを生成する

```powershell
py create_fillable_journal_pdf.py
```

正常に終わると、同じフォルダに `SelfCareJournal_fillable.pdf` が作成されます。

別のファイル名や場所に出力したい場合は、次のように指定できます。

```powershell
py create_fillable_journal_pdf.py --input SelfCareJournal_print_final.pdf.pdf --output SelfCareJournal_fillable.pdf
```

## Macでの実行手順

### 1. Pythonを確認する

ターミナルを開いて、次を実行します。

```bash
python3 --version
```

Python 3のバージョンが表示されればOKです。表示されない場合は、HomebrewやPython公式サイトからPython 3をインストールしてください。

### 2. このフォルダへ移動する

例：デスクトップにこのリポジトリを置いた場合。

```bash
cd ~/Desktop/self-care-journal
```

### 3. 必要なライブラリを入れる

```bash
python3 -m pip install -r requirements.txt
```

もし `pip` が古いと言われる場合は、先に次を実行してから再度インストールしてください。

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### 4. PDFを生成する

```bash
python3 create_fillable_journal_pdf.py
```

正常に終わると、同じフォルダに `SelfCareJournal_fillable.pdf` が作成されます。

別のファイル名や場所に出力したい場合は、次のように指定できます。

```bash
python3 create_fillable_journal_pdf.py --input SelfCareJournal_print_final.pdf.pdf --output SelfCareJournal_fillable.pdf
```

## 出力されたPDFの確認方法

### PCで確認する

1. `SelfCareJournal_fillable.pdf` を開きます。
2. P3のチェックボックスをクリックして、チェックが入るか確認します。
3. P5の記入欄に文字を入力できるか確認します。
4. P7のチェックボックス、「その他」欄、下部記入欄を確認します。
5. P9の Blog / note / X をクリックして、リンクが開くか確認します。
6. 入力後に保存し、閉じてから再度開いて、入力内容が残っているか確認します。

### iPhoneの「ファイル」アプリで確認する

1. `SelfCareJournal_fillable.pdf` をiCloud Drive、AirDrop、メール、またはFinder経由でiPhoneへ送ります。
2. iPhoneの「ファイル」アプリでPDFを開きます。
3. P3とP7のチェックボックスをタップして、チェックできるか確認します。
4. P5とP7の記入欄をタップして、キーボード入力できるか確認します。
5. P9の Blog / note / X をタップして、リンクが開くか確認します。
6. 入力後にPDFを閉じ、もう一度開いて入力内容が残るか確認します。

## よくあるエラーと対処法

### `pypdf is not installed` と表示される

`pypdf` が入っていません。次を実行してください。

Windows:

```powershell
py -m pip install -r requirements.txt
```

Mac:

```bash
python3 -m pip install -r requirements.txt
```

### `Input PDF not found` と表示される

入力PDF `SelfCareJournal_print_final.pdf.pdf` がスクリプトと同じフォルダにありません。

対処法:

- `SelfCareJournal_print_final.pdf.pdf` をこのフォルダに置いてから再実行する。
- または `--input` で入力PDFの場所を指定する。

例:

```bash
python3 create_fillable_journal_pdf.py --input /path/to/SelfCareJournal_print_final.pdf.pdf --output SelfCareJournal_fillable.pdf
```

### Windowsで `py` が見つからない

Pythonがインストールされていないか、PATHに入っていません。

対処法:

- Microsoft StoreまたはPython公式サイトからPython 3をインストールする。
- インストール時に `Add python.exe to PATH` を有効にする。
- `py` の代わりに `python` または `python3` を試す。

```powershell
python --version
python create_fillable_journal_pdf.py
```

### Macで `python3` が見つからない

Python 3がインストールされていません。

Homebrewがある場合:

```bash
brew install python
```

その後、再度確認してください。

```bash
python3 --version
```

### PDFはできたが、チェックや入力が反応しない

PDFビューアがフォーム入力に対応していない可能性があります。

対処法:

- iPhoneでは「ファイル」アプリで開く。
- PCではAdobe Acrobat Reader、Preview、Edge、Chromeなど別のビューアで開く。
- ブラウザ表示で反応しない場合は、PDFをダウンロードしてからローカルアプリで開く。

### 入力内容を保存できない

ビューアがフォーム保存に対応していない、または読み取り専用の場所で開いている可能性があります。

対処法:

- PDFをローカルフォルダにコピーしてから開く。
- 入力後に「保存」または「別名で保存」を実行する。
- iPhoneでは「ファイル」アプリ内のiCloud DriveまたはこのiPhone内に置いて確認する。

## 開発者向けメモ

フォーム位置はA4ページサイズ `595.2756 x 841.8898 pt` のPDF座標で指定しています。位置を調整する場合は、`create_fillable_journal_pdf.py` 内の `CHECKBOXES`、`TEXT_FIELDS`、`LINKS` を編集してください。
