# Gradioから、Pythonコードを抽出するメインプログラム
# (1) タグ名: URIのDemoプログラムを抜き出す。
# (2-1) タグ名: URIの 情報を抜き出す。
# (2-2) 抜き出した情報(プログラム)を保存する。
#       ------ここまで。
# (3-1) [GPT-4] 取得したデータで、Fine-Tuning用のデータを作成
# (3-2) [GptForAll] [GPT-4] 取得したデータで、Fine-Tuning用のデータを作成
# (4-1) [GPT-4] 取得したデータで、Fine-Tuning する。
# (4-2) [GptForAll-Local] 取得したデータで、Fine-Tuning する。
# (5) 利用評価
from crawl_python_code import CrawlerPythonCode
import pprint
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class CrawlerCode:
    def __init__(self):
        self.json_dir = './data/json/'
        self.json_path = os.path.join(os.getcwd(), self.json_dir)

    def get_submenu_to_json_path(self):
        # ディレクトリの確認と作成、ディレクトリが存在しない場合は作成
        if not os.path.exists(self.json_path):
            os.makedirs(self.json_path)

        # function_name: function_url.jsonファイルのパス
        function_url_path = os.path.join(self.json_dir, 'function_url.json')

        # ChromeDriverのパスをServiceオブジェクトとして指定
        s = Service('/opt/homebrew/bin/chromedriver')  # ここにchromedriverの絶対パスを指定
        driver = webdriver.Chrome(service=s)

        # GradioのWebページにアクセス
        driver.get("https://www.gradio.app")

        # WebDriverWaitを使用して、"Docs"リンクが表示されるまで最大10秒間待つ
        # CSSセレクタを使用して"Docs"リンクを見つける
        docs_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/docs"]'))
        )
        docs_button.click()

        # ページが完全にロードされるのを待つために少し待つ
        time.sleep(5)

        # 遷移後のページ内のすべてのリンクを取得
        links = driver.find_elements(By.CSS_SELECTOR, 'a.thin-link')

        # リンクのテキストとURLの一覧を表示
        links_data = {}
        for link in links:
            text = link.text
            href = link.get_attribute('href')
            if href[-1] == '/':
                links_data[text] = href

        # jsonファイルとして保存
        with open(function_url_path, 'w') as file:
            json.dump(links_data, file, ensure_ascii=False, indent=4)

        print(f"リンクデータは '{function_url_path}' に保存されました。")

        # ブラウザを閉じる
        time.sleep(5)
        driver.quit()
        return True

    def crawler_get_code(self):
        # [function_url.json] GradioのURL：サブメニューから、サブメニュー：URL　のデータ　
        self.get_submenu_to_json_path()

        # [function_name.html] → HTMLファイルの作成

        # function_url.jsonの読み込み
        with open('./data/json/function_url.json', 'r') as fp:
            function_url_data = json.load(fp)

        # python-codeを取り出し、functionごとのファイルを作成する。
        for function_name, function_url in function_url_data.items():
            print('[{}] -> [{}]'.format(function_name, function_url))

            # python codeの取り出し
            crawler = CrawlerPythonCode(function_url)
            div_class = "codeblock"  # 抽出したいdivのクラス名
            code_blocks = crawler.run(div_class)
            function_name = function_url.split("/")[-2]  # function名を抽出する。

            file_name = './data/code/' + function_name + '.json'
            with open(file_name, 'w') as f:
                f.write(json.dumps(code_blocks))


# テストコード
instance = CrawlerCode()
instance.crawler_get_code()
