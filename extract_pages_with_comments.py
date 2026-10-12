#!/usr/bin/env python3
"""注釈（コメント）があるページだけを抜き出して、新しいPDFにする。

入力がPDFファイルならその1件を、フォルダなら直下のPDFをすべて処理する。
注釈があるページが1つもなければ、出力ファイルは作らない。

出力名を省略したときは、元の名前の末尾に「_extract」を付ける。
フォルダ入力で出力先を省略したときは、入力フォルダと同じ場所に保存する。

依存: Python 3、PyMuPDF（pip install pymupdf）

例:
  python3 extract_pages_with_comments.py input.pdf -o output.pdf
  python3 extract_pages_with_comments.py input.pdf
  python3 extract_pages_with_comments.py ./pdfs -o ./out
  python3 extract_pages_with_comments.py ./pdfs
"""

import os
import sys
import argparse
import fitz  # PyMuPDF


def extract_pages_with_comments(input_pdf, output_pdf):
    """1つのPDFから注釈があるページだけを抜き出して output_pdf に保存する。

    該当ページがなければファイルは作らず、その旨を表示する。
    """
    try:
        document = fitz.open(input_pdf)
        writer = fitz.open()
        pages_with_comments = []

        for page_num in range(document.page_count):
            page = document.load_page(page_num)
            if page.first_annot:
                writer.insert_pdf(document, from_page=page_num, to_page=page_num)
                pages_with_comments.append(page_num + 1)

        if pages_with_comments:
            writer.save(output_pdf)
            writer.close()
            print(f"[OK] 注釈があるページを抽出して {output_pdf} に保存しました")
            print(f"     抽出したページ番号: {pages_with_comments}")
        else:
            print(f"[INFO] {input_pdf} に注釈があるページはありません")
            print("       出力ファイルは作成しません")

        document.close()

    except Exception as e:
        print(f"[ERROR] PDFの処理中にエラーが発生しました: {e}")


def make_output_path(input_path, output_arg):
    """ファイル入力のときの出力パスを決める。

    output_arg があればそれを使う。なければ同じディレクトリに「_extract」を付けた名前を作る。
    """
    if output_arg:
        return output_arg
    dir_name = os.path.dirname(input_path)
    base, ext = os.path.splitext(os.path.basename(input_path))
    output_filename = f"{base}_extract{ext}"
    return os.path.join(dir_name, output_filename)


def main():
    parser = argparse.ArgumentParser(
        description="注釈があるページだけを抽出して、新しいPDFにまとめる"
    )
    parser.add_argument(
        "input_path",
        help="入力PDF、またはPDFが入ったフォルダ"
    )
    parser.add_argument(
        "-o", "--output",
        help="出力ファイル（入力がファイルのとき）または出力フォルダ（入力がフォルダのとき）",
        default=None
    )
    args = parser.parse_args()

    input_path = args.input_path
    output_arg = args.output

    if not os.path.exists(input_path):
        print(f"[ERROR] 入力パスがありません: {input_path}")
        sys.exit(1)

    if os.path.isfile(input_path):
        _, ext = os.path.splitext(input_path)
        if ext.lower() != ".pdf":
            print(f"[ERROR] PDFファイルを指定してください: {input_path}")
            sys.exit(1)

        output_pdf = make_output_path(input_path, output_arg)
        output_dir = os.path.dirname(output_pdf)
        if output_dir and not os.path.isdir(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        extract_pages_with_comments(input_path, output_pdf)

    elif os.path.isdir(input_path):
        input_dir = input_path

        if output_arg:
            output_dir = output_arg
        else:
            output_dir = input_dir

        if not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                print(f"[ERROR] 出力フォルダを作成できません: {output_dir} -> {e}")
                sys.exit(1)

        pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]

        if not pdf_files:
            print(f"[INFO] フォルダ内にPDFがありません: {input_dir}")
            sys.exit(0)

        for filename in pdf_files:
            input_pdf = os.path.join(input_dir, filename)
            base, ext = os.path.splitext(filename)
            output_filename = f"{base}_extract{ext}"
            output_pdf = os.path.join(output_dir, output_filename)
            extract_pages_with_comments(input_pdf, output_pdf)

    else:
        print(f"[ERROR] 入力パスがファイルでもフォルダでもありません: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
