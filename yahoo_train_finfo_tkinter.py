from tkinter import *
import tkinter.ttk as ttk
import os
import requests
from bs4 import BeautifulSoup

from PIL import Image, ImageTk
from datetime import datetime, timedelta
import time
import textwrap
# アイコン画像の下には取得した文字列をそのまま表示
# メインウィンドウ作成
root = Tk()

# メインウィンドウサイズ
root.geometry("1024x600")

# メインウィンドウタイトル
root.title("info")
url_dict = {
    "山手線": 'https://transit.yahoo.co.jp/traininfo/detail/21/0/', "中央線": 'https://transit.yahoo.co.jp/traininfo/detail/38/0/',
    "埼京線": 'https://transit.yahoo.co.jp/traininfo/detail/50/0/', "湘南新宿ライン": 'https://transit.yahoo.co.jp/traininfo/detail/25/0/',"銚子電鉄":'https://transit.yahoo.co.jp/traininfo/detail/181/0/'
}
train_list = [
    "中央線", "山手線", "埼京線", "湘南新宿ライン","銚子電鉄"
]

# MainFrame クラス


class MainFrame(ttk.Frame):
    # コンストラクタ
    def __init__(self, master=None, **kwargs):
        # 親クラスのコンストラクタを呼び出す
        super().__init__(master, **kwargs)

        # create_widgets を呼び出す
        self.create_widgets()

    # ウィジェットを作成
    def create_widgets(self):
        # フレームを作成
        self.frame = Frame(self, bg="AntiqueWhite2", bd=0, height=200, relief="flat")

        # フレームを配置
        self.frame.grid(row=0, column=0, columnspan=8, sticky="news")

        # このスクリプトの絶対パス
        self.scr_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        #タイトルの表示
        self.wt=Label(self.frame, text="路線の運行情報", bg="AntiqueWhite2", font=("", 80))
        self.wt.place(width=800, x=100, y=10)

        # 運行情報アイコンパス（ディクショナリ）
        self.icon_dict = {
            "normal": Image.open(self.scr_path + "/img/train.png"), "trouble": Image.open(self.scr_path + "/img/warning.png")
        }

        # アイコンサイズを画面サイズにフィット（64x64）させる
        for key, value in self.icon_dict.items():
            self.icon_dict[key] = self.icon_dict[key].resize(
                (64, 64), Image.ANTIALIAS)
            self.icon_dict[key] = ImageTk.PhotoImage(self.icon_dict[key])

        # 路線リスト
        self.wwl = [
            Label(self, text="中央線",  bg="red", font=("", 30, "bold")),
            Label(self, text="山手線",  bg="lawn green", font=("", 30, "bold")),
            Label(self, text="埼京線",  bg="green", font=("", 30, "bold")),
            Label(self, text="湘南新宿ライン", bg="orange", font=("", 30, "bold")),
            Label(self, text="銚子電鉄", bg="DarkOrange", font=("", 30, "bold"))

        ]

        # 路線を配置
        for i in range(len(self.wwl)):
            self.wwl[i].grid(row=1, column=i, sticky="news")

        # 運行アイコンの初期配置辞書
        self.wwi = [
            Label(self, image=self.icon_dict["normal"], bg="white"),
            Label(self, image=self.icon_dict["normal"], bg="white"),
            Label(self, image=self.icon_dict["normal"], bg="white"),
            Label(self, image=self.icon_dict["normal"], bg="white"),
            Label(self, image=self.icon_dict["normal"], bg="white")
        ]

        # 運行アイコンを配置
        for i in range(len(self.wwi)):
            self.wwi[i].grid(row=2, column=i, sticky="news")

        # 運転状況
        self.wwt = [
            Label(self, text="0", bg="white", font=("", 20)),
            Label(self, text="0", bg="white", font=("", 20)),
            Label(self, text="0", bg="white", font=("", 20)),
            Label(self, text="0", bg="white", font=("", 20)),
            Label(self, text="0", bg="white", font=("", 20))

        ]

        # 運転状況を配置
        for i in range(len(self.wwt)):
            self.wwt[i].grid(row=3, column=i, sticky="news")

        # レイアウト
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        for i in range(len(self.wwl)):
            self.columnconfigure(i, weight=1)


# メインフレームを配置
app = MainFrame(root)
app.pack(side=TOP, expand=1, fill=BOTH)

# メインウィンドウを閉じる


def wm_close():
    root.destroy()


# 閉じるボタン作成
btn = Button(root, text=" X ", font=('', 16), relief=FLAT, command=wm_close)

# 画面がリサイズされたとき


def change_size(event):
    # ボタンの位置を右上に
    btn.place(x=root.winfo_width() - 60, y=14)


# 画面のリサイズをバインドする
root.bind('<Configure>', change_size)

# メインウィンドウの最大化
#root.attributes("-zoom", "1")
root.attributes("-fullscreen", "1")

# 常に最前面に表示
root.attributes("-topmost", True)


def update_train_info():

    count = 0
    app.wt
    # 登録路線の運行情報を取得
    for item in train_list:
        web_requests = requests.get(url_dict[item])

        # BeautifulSoupを利用してWebページを解析する
        soup = BeautifulSoup(
            web_requests.text, 'html.parser')
            
        # .findでtroubleクラスのddタグを探す
        if soup.find('dd', class_='normal'):
            status = "normal"
            trouble_text="平常運転"
            bg="green yellow"
        else:
            status = "trouble"
            text_list=textwrap.wrap(soup.find('dd',class_='trouble').get_text(), 10)
            trouble_text='\n'.join(text_list)
            bg="red4"
        app.wwl[count].configure(text=item)  # 路線名の表示
        # 運行情報アイコンで表示
        app.wwi[count].configure(image=app.icon_dict[status],bg=bg)

        # 運行情報を表示
        app.wwt[count].configure(text="{0}".format(trouble_text),bg="AntiqueWhite2")

        # 表示カウンタを更新
        count += 1

    return


# 初回起動
update_train_info()

# コールバック関数を登録

root.after(300000, update_train_info)

# メインループ
root.mainloop()
