import pathlib
import re
from io import StringIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import pdf2image


# 準備したい講座回数・資料PDFファイルのパス・画像出力先フォルダのパスを記入
cource = 2
pdf_filepath = pathlib.Path('/Users/m.ohsaki/Dropbox/○MyDataBox/ノンプロ研/20200930初心者講座Pythonコース-02.pdf')
output_dirpath = pathlib.Path('/Users/m.ohsaki/Dropbox/○MyDataBox/ノンプロ研/Python初級講座4期')

# PDFファイルからテキスト抽出
# TODO: open, closeをwith文で書く
pdf_file = open(pdf_filepath, 'rb')  # PDFファイルオブジェクトを生成
serch_text = r'演習\s*\d－\d+'  # 抽出する文字列(正規表現：ここでは「演習○－○」)
output_pages = {}
page_num = 1

for page in PDFPage.get_pages(pdf_file):
    # 初期化
    # TODO: あとでpdfminerの使い方をまとめる
    rsrcmgr = PDFResourceManager()
    outfp = StringIO()
    codec = 'utf-8'
    laparams = LAParams(detect_vertical=True)
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    interpreter.process_page(page)

    # 出力テキストの整形・演習番号を正規表現で抽出
    output_text = outfp.getvalue().replace('\u2028', '').split('Copyright')[0].rstrip()
    output_series = re.match(serch_text, outfp.getvalue())

    # 演習問題リスト作成
    if output_series:
        output_pages[page_num] = (output_series.group(), output_text)

    page_num += 1

pdf_file.close()
# device.close()
# retstr.clos()
# TODO:読解 https://tech.bita.jp/article/18

# テキストファイル出力
# TODO: テキストをテーブルっぽく整形してファイル出力したい
output_text_path = output_dirpath / f'0{cource}_ensyu.txt'
with output_text_path.open('w') as f:
    print(output_pages, file=f)

# 画像ファイル出力
# TODO: あとでpdf2imageの使い方をまとめる
# - convert_from_path関数には1ページごとの画像のリストが入る
# - mkidr(exist_ok)にすると上書きされるっぽい
img_dirpath = output_dirpath / f'0{cource}'
pathlib.Path(img_dirpath).mkdir(exist_ok=True)

images = pdf2image.convert_from_path(pdf_filepath, size=1280)
for index, image in enumerate(images):
    if index+1 in output_pages:
        filename = output_pages[index+1][0].replace(' ', '')
        image_filepath = img_dirpath / f'{filename}.png'
        image.save(image_filepath)
