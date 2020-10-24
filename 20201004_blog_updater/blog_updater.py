#############
# Markdownブログ執筆支援
# PelicanブログをGitHubPagesにアップロードするGUIツール
#############


import pathlib
import os
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import ttk


MY_GITHUB_PAGE = '<ブログアップロード用のGithubページ>'
MY_BLOG_URL = '<ブログURL>'
MY_DIRPATH = pathlib.Path(
    '<ブログのプロジェクトフォルダのパス>'
)

ARTICLES_DIRPATH = pathlib.Path(
    '<contentフォルダ（MY_DIRPATH/content）>'
)
OUTPUTS_DIRPATH = pathlib.Path(
    '<outputフォルダ（MY_DIRPATH/output）>'
)

CATEGORIES = (
    'Category1', 'Category2', 'Category3',
)

PROJECTS = {
    '': '',
    'Project1': 'p1',
    'Project2': 'p2',
    'Project3': 'p3',
}


# メインウィンドウの作成
root = tk.Tk()
root.title('blog updater')
root.geometry('300x300+50+100')

# uploadラベル付きフレームの作成・配置
upload_frame = ttk.LabelFrame(
    text='upload',
    labelanchor='n',
    width=280,
    height=50
)
upload_frame.pack()
upload_frame.propagate(False)

# uploadボタンとチェックボックスの作成・配置
push_flg = tk.BooleanVar()
push_flg.set(True)
upload_btn = ttk.Button(
    upload_frame,
    text='upload',
    command=lambda: upload_blog(push_flg)
)
check_btn = ttk.Checkbutton(
    upload_frame,
    variable=push_flg,
    text='Githubにpushする'
)
upload_btn.pack(side='left')
check_btn.pack()

# createラベルつきフレームの作成・配置
create_frame = ttk.LabelFrame(
    text='create',
    labelanchor='n',
    width=280,
    height=200
)
create_frame.pack()
create_frame.propagate(False)

# createボタンの作成・配置
create_btn = ttk.Button(
    create_frame,
    text='create',
    command=lambda: create_article(title_var.get(), slug_var.get(), category_var.get(), project_var.get())
)
create_btn.pack(side='left')

# projectラベル・コンボボックスの作成・設置
project_label = ttk.Label(create_frame, text='プロジェクト名を選択')
project_var = tk.StringVar()
project_cb = ttk.Combobox(create_frame, textvariable=project_var)
project_cb.bind(
    '<<ComboboxSelected>>',
    lambda e: select_project(project_var.get())
)
project_cb['values'] = list(PROJECTS)
project_cb.set(list(PROJECTS)[0])
project_label.pack()
project_cb.pack()

# title, slugラベル・テキストボックスの作成・配置
title_label = ttk.Label(create_frame, text='記事タイトル')
title_var = tk.StringVar()
title_entry = ttk.Entry(create_frame, textvariable=title_var)
title_label.pack()
title_entry.pack()

slug_label = ttk.Label(create_frame, text='記事URL')
slug_var = tk.StringVar()
slug_entry = ttk.Entry(create_frame, textvariable=slug_var)
slug_label.pack()
slug_entry.pack()

# categoryラベル・コンボボックスの作成・設置
category_label = ttk.Label(create_frame, text='記事カテゴリー')
category_var = tk.StringVar()
category_cb = ttk.Combobox(create_frame, textvariable=category_var)
category_cb.bind(
    '<<ComboboxSelected>>',
    lambda e: print(category_var.get())
)
category_cb['values'] = CATEGORIES
category_cb.set(CATEGORIES[0])
category_label.pack()
category_cb.pack()

# stdoutラベル付きフレームの作成・配置
stdout_frame = ttk.LabelFrame(
    text='stdout',
    labelanchor='n',
    width=280,
    height=50
)
stdout_frame.pack()
stdout_frame.propagate(False)

# stdoutテキストボックスの作成・設置
stdout_var = tk.StringVar()
stdout_entry = ttk.Entry(stdout_frame, textvariable=stdout_var, width=280)
stdout_entry.pack()


def change_dir():
    os.chdir('/')
    os.chdir(MY_DIRPATH)


def upload_blog(push_flg):
    """ブログをアップロードする関数"""
    try:
        change_dir()  # ブログプロジェクトのディレクトリに自動で入る'
        msg = 'Now uploading...'
        stdout_var.set(msg)
        print(msg)
        # subprocess.run(['make', 'html'])
        # subprocess.run(['make', 'publish'])
        # subprocess.run(['ghp-import', OUTPUTS_DIRPATH])
        # subprocess.run(['git', 'push', MY_GITHUB_PAGE, 'gh-pages:master'])
        subprocess.run(['pelican', 'content', '-o', 'output', '-s', 'pelicanconf.py'])
        subprocess.run(['ghp-import', 'output', '-b', 'master'])
        subprocess.run(['git', 'push', MY_GITHUB_PAGE, 'gh-pages:master'])
        msg = f'Uploading is completed! \n{MY_BLOG_URL}'
        stdout_var.set(msg)
        print(msg)
        if push_flg.get():
            push_to_github()
    except Exception as exc:
        msg = f'Failed to upload the blog. \n{str(exc)}'
        stdout_var.set(msg)
        print(msg)


def push_to_github():
    """Githubにバックアップをプッシュする関数"""
    today = datetime.now().strftime('%Y%m%d')
    commit_msg = '\"' + today + ' ' + 'Update' + '\"'

    try:
        msg = 'Now pushing for github... '
        stdout_var.set(msg)
        print(msg)
        subprocess.call(['git', 'add', '.'])
        subprocess.call(['git', 'commit', '-m', commit_msg])
        subprocess.call(['git', 'push', 'origin', 'master'])
        msg = 'Pushing for github is completed!'
        stdout_var.set(msg)
        print(msg)
    except Exception as exc:
        msg = f'Failed to push for github. \n{str(exc)}'
        stdout_var.set(msg)
        print(msg)


def get_disp_time():
    today = datetime.now()
    disp_time = {
        'year': str(today.year),
        'month': str(today.month).zfill(2),
        'day': str(today.day).zfill(2),
        'hour': str(today.hour).zfill(2),
        'minute': str(today.minute).zfill(2)
    }
    return disp_time


def make_template(title, slug, category):
    disp_time = get_disp_time()
    template = f"""title: {title}
Slug: {slug}
Date: {disp_time['year']}-{disp_time['month']}-{disp_time['day']} {disp_time['hour']}:{disp_time['minute']}
Category: {category}
Tags:
Summary:\n
"""
    return template


def get_next_serial(project):
    project_dirpath = ARTICLES_DIRPATH / CATEGORIES[1] / PROJECTS[project]
    project_files = list(project_dirpath.iterdir())
    slice_index = 10 + len(PROJECTS[project])
    max_serial = 0
    for file in project_files:
        filename = file.name
        if int(filename[slice_index:-3]) > max_serial:
            max_serial = int(filename[slice_index:-3])
    return max_serial + 1


def make_template_by_project(project):
    disp_time = get_disp_time()
    serial = get_next_serial(project)
    title = f'[{project}{str(serial).zfill(2)}]'
    slug = f'dev-{PROJECTS[project]}{str(serial).zfill(2)}'

    template = f"""title: {title}
Slug: {slug}
Date: {disp_time['year']}-{disp_time['month']}-{disp_time['day']} {disp_time['hour']}:{disp_time['minute']}
Category: Work
Tags: {PROJECTS[project]}
Summary:\n
## はじめに
### 方針
### 今回のアジェンダ\n\
## MEMO\n\
## おわりに
### 一言
### 今後の方針'''
"""
    return template


def set_default():
    # 0文字目から最後までテキストボックスの値を削除
    title_entry.delete(0, tk.END)
    slug_entry.delete(0, tk.END)
    category_cb.set(CATEGORIES[0])
    project_cb.set(PROJECTS[''])


def select_project(project):
    title_entry.config(state=(tk.DISABLED if project else tk.NORMAL))
    slug_entry.config(state=(tk.DISABLED if project else tk.NORMAL))
    category_cb.config(state=(tk.DISABLED if project else tk.NORMAL))


def create_article(title, slug, category, project):
    disp_time = get_disp_time()
    disp_time = f"{disp_time['year']}{disp_time['month']}{disp_time['day']}"

    if bool(title and slug) or project:
        if project:
            # project名を選択したケース
            # 保存ファイルパスはcontent/work/<project>/<date>_<project>_<no>.md
            template = make_template_by_project(project)
            article_dirpath = ARTICLES_DIRPATH / CATEGORIES[1] / PROJECTS[project]
            slug = f'{PROJECTS[project]}_{get_next_serial(project)}'
        else:
            # projectではなくtitle, slug, categoryを選択したケース
            # 保存ファイルパスはcontent/<category>/<date>_<project>_<no>.md
            template = make_template(title, slug, category)
            article_dirpath = ARTICLES_DIRPATH / category.lower()
        if not os.path.exists(article_dirpath):
            os.mkdir(article_dirpath)
        article_filepath = article_dirpath / (disp_time + '_' + slug + '.md')

        try:
            with open(article_filepath, mode='x') as newfile:
                newfile.write(template)
            set_default()
            msg = 'Success to create new file.'
            stdout_var.set(msg)
            print(msg)

        except FileExistsError as e:
            msg = f'Some error occurd. \n{e}'
            stdout_var.set(msg)
            print(msg)

    else:
        msg = 'Select Project, or enter Title and Slug'
        stdout_var.set(msg)
        print(msg)


# メインウィンドウ表示
if __name__ == '__main__':
    root.mainloop()
