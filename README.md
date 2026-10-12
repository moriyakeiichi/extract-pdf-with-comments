# 注釈ページ抽出

注釈の付いたページだけを抜き出して、新しい PDF にまとめる Mac アプリです。

Apple Silicon（M1以降）、macOS 13 以降で動きます。処理は Mac の中だけで行い、PDF を外部へ送りません。

## アプリを入手する

[Releases](https://github.com/moriyakeiichi/extract-pdf-with-comments/releases/latest) の `extract-pdf-with-comments-mac.zip` をダウンロードし、展開して `注釈ページ抽出.app` を開きます。

初回に「開発元を確認できない」と出たときは、アプリを右クリックして「開く」を選んでください。Apple の公証は行っていません。

操作、抽出条件、前後ページの追加、コマンド版の使い方は [使い方.md](使い方.md) にまとめています。

## ソースからビルドする

```sh
python3 -m venv .build-env
.build-env/bin/python -m pip install -r requirements-build.txt
.build-env/bin/python -m unittest discover -s tests -v
.build-env/bin/python build_apps.py
```

`nya_extract_pages_with_comments.py` は、注釈があるページの抽出をコマンドから行うスクリプトです。

## ライセンス

アプリは PyMuPDF（AGPL-3.0）と Python を同梱しています。ライセンス原文はアプリ内の `Contents/Resources/Licenses` にあります。このリポジトリが、配布するアプリに対応するソースです。
