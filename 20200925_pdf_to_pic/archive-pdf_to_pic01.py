import os
import pathlib
import re
from io import StringIO
import glob

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import pdf2image


lesson = int(input('第何回の講座の準備をする？'))

nonpro_dirpath = pathlib.Path('/Users/m.ohsaki/Dropbox/○MyDataBox/ノンプロ研/')
output_dirpath = os.path.join(nonpro_dirpath, 'Python初級講座4期')

# 講座資料pdfを取得
os.chdir(nonpro_dirpath)
lesson_resumes = glob.glob('*.pdf')
lesson_resumes = sorted(lesson_resumes)
pdf_filepath = os.path.join(nonpro_dirpath, lesson_resumes[lesson-1])

# PDFファイルからテキスト抽出
pdf_file = open(pdf_filepath, 'rb') # PDFファイルオブジェクトを生成
serch_text = r'演習\s*\d－\d+' # 抽出する文字列(正規表現)
output_pages = {}
page_num = 1

for page in PDFPage.get_pages(pdf_file):
    #逐次初期化
    # - あとでpdfminerの使い方をまとめる
    rsrcmgr = PDFResourceManager()
    outfp = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    laparams.detext_vertical = True
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

# テキスト保存
output_text_path = pathlib.Path(os.path.join(output_dirpath, f'0{lesson}_ensyu.txt'))
with output_text_path.open('w') as f:
    print(output_pages, file=f)

# 画像保存
# - convert_from_path関数には1ページごとの画像のリストが入る
img_dirpath = os.path.join(output_dirpath, f'0{lesson}')

images = pdf2image.convert_from_path(pdf_filepath, size=1280)
for index, image in enumerate(images):
    if index+1 in output_pages:
        filename = output_pages[index+1][0].replace(' ', '')
        image.save(os.path.join(img_dirpath, f'{filename}.png'))