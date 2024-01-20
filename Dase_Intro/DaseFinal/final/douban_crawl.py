import requests
import pprint
import re
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT10.0; Win64; x64)AppleWebKit/537.36(KHTML, '
                  'like Gecko)Chrome/120.0.0.0Safari/537.36 Edg/120.0.0.0'
}
# 用于应对反爬机制，作为请求头

# 构造分页数字列表
page_indexes = range(0, 250, 25)


# 用于下载所有页面的内容，一共十个页面
def download_all_htmls():
    webs = []
    for index in page_indexes:
        url = f"https://movie.douban.com/top250?start={index}&filter="
        # {index}用于分页查找的定位功能
        # print("crawl html:", url)
        r = requests.get(url, headers=headers)
        # 验证网页是否被成功爬取，r.status_code为200即证明爬取成功
        if r.status_code != 200:
            raise Exception("error")
        webs.append(r.text)
        # 将网页加入列表webs
    return webs


htmls = download_all_htmls()


def parse_single_html(html_text):
    # 解析单个网页的数据
    soup = BeautifulSoup(html_text, 'html.parser')
    # 下面是各种定位找要爬取的信息，通过html的标签进行查找
    article_items = (
        soup.find("div", class_="article")
        .find("ol", class_="grid_view")
        .find_all("div", class_="item")
    )
    datas = []
    for article_item in article_items:
        rank = article_item.find("div", class_="pic").find("em").get_text()
        info = article_item.find("div", class_="info")
        title = info.find("div", class_="hd").find("span", class_="title").get_text()
        OtherInfo = info.find("div", class_="bd").find("p", class_="").get_text()
        stars = (
            info.find("div", class_="bd")
            .find("div", class_="star")
            .find_all("span")
        )
        rating_star = stars[0]["class"]
        # 获取了span标签的class的值
        rating_num = stars[1].get_text()
        comments = stars[3].get_text()
        years = re.search(pattern=r"\d{4}", string=OtherInfo)
        something = re.search(pattern=r"/\d{4}.(\/).+(\/).+/", string=OtherInfo)
        thing = re.compile(r"\d{4}.(\/).")
        location = thing.sub("", something.group())
        country = re.compile(r".(\/).+")
        nation = country.sub("", location)
        kind = re.compile(r".+(\/).")
        types = kind.sub("", location)

        datas.append({
            "rank": rank,
            "title": title,
            "years": years,
            "location": nation,
            "type": types,
            # "rating_star": rating_star.replace("rating", "").replace("-t", ""),
            # 获得的初始内容为rating5-t，通过replace前后内容能够得到我们想要的结果
            "rating_num": rating_num,
            "comments": comments.replace("人评价", "")
        })
    return datas


all_datas = []
for html in htmls:
    all_datas.extend(parse_single_html(html))

df = pd.DataFrame(all_datas)
# 通过DataFrame来构造数据列表用于形成Excel文件
df.to_excel("./豆瓣电影Top250.xlsx")
# pprint.pprint(parse_single_html(htmls[0]))
