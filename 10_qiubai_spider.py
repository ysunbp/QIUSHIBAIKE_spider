from lxml import etree
import requests
import json


class QiubaiSpider:

    def __init__(self):
        self.url_temp = "https://www.qiushibaike.com/hot/page/{}/"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"}

    def get_url_list(self):
        url_list = [self.url_temp.format(i) for i in range(1,14)]
        return url_list

    def parse_url(self, url):
        response = requests.get(url, headers = self.headers)
        return response.content.decode()

    def get_content_list(self, html_str):
        html = etree.HTML(html_str)
        div_list = html.xpath("//div[@class = 'article block untagged mb15 typs_hot']")
        content_list = []
        for div in div_list:
            item = {}
            item["author"] = div.xpath(".//h2/text()")[0].strip() if len(div.xpath(".//h2/text()"))>0 else None
            item["content"] = div.xpath(".//div[@class = 'content']/span/text()")
            item["content"] = [i.strip() for i in item["content"]]
            item["stats_vote"] = div.xpath(".//span[@class = 'stats-vote']/i/text()")[0] if len(div.xpath(".//span[@class = 'stats-vote']/i/text()"))>0 else None
            item["stats_comments"] = div.xpath(".//span[@class = 'stats-comments']//i/text()")[0] if len(div.xpath(".//span[@class = 'stats-comments']//i/text()"))>0 else None
            content_list.append(item)
        return content_list

    def save_content_list(self,content_list):
        with open("qiubai.txt", "a", encoding = "utf-8")as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n")
        print("*"*100)

    def run(self):
        #1. 根据url地址的规律构造列表
        url_list = self.get_url_list()
        #2. 发送请求获取数据
        for url in url_list:
            html_str = self.parse_url(url)
        #3. 获取响应，提取数据
            content_list = self.get_content_list(html_str)
        #4. 保存
            self.save_content_list(content_list)

if __name__ == '__main__':
    qiubai = QiubaiSpider()
    qiubai.run()
