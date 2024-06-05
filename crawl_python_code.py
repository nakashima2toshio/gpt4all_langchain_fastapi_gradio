#
from typing import Any, List, Optional

import autopep8
import requests
from bs4 import BeautifulSoup


class CrawlerPythonCode:
    def __init__(self, url: str):
        self.id_code_json = None
        self.url = url
        self.response = None
        self.soup = None
        self.divs = None

    def fetch_html(self) -> Optional[requests.Response]:
        self.response = requests.get(self.url)
        if self.response.status_code != 200:
            print("Failed to retrieve the webpage")
            return None
        return self.response

    def extract_divs(self, div_class: str) -> List[BeautifulSoup]:
        if not self.response:
            return []
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.divs = self.soup.find_all("div", {"class": div_class})
        return self.divs

    def get_python_code(self, divs: List[BeautifulSoup]) -> dict[str | list[str], Any]:
        self.id_code_json = dict()
        for div in divs:
            div_id_title = div.get("id")
            if div_id_title is not None:
                code_blocks = div.find_all("code", {"class": "language-python"})
                for code_block in code_blocks:
                    python_code = code_block.text
                    formatted_code = autopep8.fix_code(python_code)
                    self.id_code_json[div_id_title] = formatted_code
        return self.id_code_json

    # example-usageのcodeもあるので、それを追加する。
    def get_example_code(self, divs: List[BeautifulSoup]):
        div_id = 'example-usage'
        for div in self.divs:
            if div.get("id") == div_id:
                code_blocks = div.find_all("code", {"class": "language-python"})
                example_code = []
                # get_python_codeで作ったid_code_jsonに追加する
                for code_block in code_blocks:
                    python_code = code_block.text
                    formatted_code = autopep8.fix_code(python_code)
                    example_code.append(formatted_code)
                    self.id_code_json[div_id] = example_code
                return self.id_code_json

    def run(self, div_class: str) -> dict[str | list[str], Any] | dict[Any, Any]:
        if self.fetch_html():
            divs = self.extract_divs(div_class)
            self.get_python_code(divs)
            return self.get_example_code(divs)
        else:
            return self.id_code_json
