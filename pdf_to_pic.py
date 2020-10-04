import pathlib
import re
from io import StringIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import pdf2image


# ユーザー入力項目
# 準備したい講座回数・PDFファイル名をリストに記入
NO = 3
FILES = [
    '20200923初心者講座Pythonコース-01.pdf',
    '20200930初心者講座Pythonコース-02.pdf',
    '20201007初心者講座Pythonコース-03.pdf',
]
# 資料PDFファイルが保存されているフォルダのパスを記入
PDF_DIRPATH = pathlib.Path(
    '/Users/m.ohsaki/Dropbox/○MyDataBox/ノンプロ研/'
    )
PDF_FILEPATH = PDF_DIRPATH / FILES[NO-1]
# 出力先フォルダのパス
OUTPUT_DIRPATH = pathlib.Path(
    '/Users/m.ohsaki/Dropbox/○MyDataBox/ノンプロ研/Python初級講座4期'
    )
# 抽出する文字列(正規表現：ここでは「演習○－○」)
SEARCH_TEXT = r'演習\s*\d－\d+'


def get_text_from_pdf():
    """PDFファイルから演習問題に該当するテキストをページ数と共に抽出する関数
    Returns:
        output_texts(dict): 演習問題一覧。ページ数をキーとして、演習ナンバーと本文が入った辞書
    """
    # pdfminerの設定
    rsrcmgr = PDFResourceManager()
    codec = 'utf-8'
    laparams = LAParams()
    laparams.detext_vertical=True

    # PDFファイルを1ページずつ見て該当するかチェック
    output_texts = {}  # 該当するページ数とテキストを格納するdict
    with open(PDF_FILEPATH, 'rb') as fp:
        for i, page in enumerate(PDFPage.get_pages(fp)):
            outfp = StringIO()
            device = TextConverter(
                rsrcmgr,
                outfp,
                codec=codec,
                laparams=laparams
                )
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            interpreter.process_page(page)

            extracted_text = outfp.getvalue() \
                .replace('\u2028', '') \
                .split('Copyright')[0] \
                .rstrip()

            # ページ抽出：抽出条件（演習問題のページ）に該当すればTrue
            extracted_page = re.search(SEARCH_TEXT, extracted_text)

            # 演習問題のページ番号・演習番号・テキストを格納したdict作成
            if extracted_page:
                output_texts[i+1] = (extracted_page.group(), extracted_text)
    return output_texts


def save_text(output_texts):
    """演習問題一覧をテキストファイル出力
    Arg:
        output_texts(dict): 演習問題一覧。ページ数をキーとして、演習ナンバーと本文が入った辞書
    """
    output_text_path = OUTPUT_DIRPATH / f'0{NO}_ensyu.txt'
    with output_text_path.open('w') as f:
        print(output_texts, file=f)
    return None


def save_images(output_texts):
    """演習問題を画像ファイル出力
    Arg:
        contents(dict): 演習問題一覧。ページ数をキーとして、演習ナンバーと本文が入った辞書
    """
    # - convert_from_path関数には1ページごとの画像のリストが入る
    # - mkidr(exist_ok=True)にすると上書きされるっぽい
    img_dirpath = OUTPUT_DIRPATH / f'0{NO}'
    pathlib.Path(img_dirpath).mkdir(exist_ok=True)

    images = pdf2image.convert_from_path(PDF_FILEPATH, size=1280)
    for i, image in enumerate(images):
        if i+1 in contents:
            filename = contents[i+1][0].replace(' ', '')
            image_filepath = img_dirpath / f'{filename}.png'
            image.save(image_filepath)
    return None


# 実行
if __name__ == '__main__':
    contents = get_text_from_pdf()
    save_text(contents)
    save_images(contents)
