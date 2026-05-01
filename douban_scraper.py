"""
豆瓣电影 Top250 爬虫
==================
仅供学习交流使用，请勿用于商业用途或大规模爬取。
请遵守 robots.txt 及网站使用条款，合理控制爬取频率。
"""

import requests
import csv
from lxml import html
import time
import re

# ==================== 配置区域 ====================

# 数据保存路径
MOVIE_LIST_FILE = "./csv_data/douban_top250_movies.csv"

# 目标 URL
DOUBAN_TOP_URL = "https://movie.douban.com/top250"

# 【重要】请替换为你的真实 Cookie
# 获取方式：浏览器登录豆瓣 -> F12 开发者工具 -> Network -> 刷新页面 -> 复制 Cookie
COOKIE = '''请在此处粘贴你的 Cookie'''
# 请求头配置（模拟浏览器行为）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://www.douban.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cookie": COOKIE
}


# ==================== 核心功能 ====================

def get_movie_info(movie_info_url):
    """
    获取单部电影的详细信息

    Args:
        movie_info_url: 电影详情页 URL

    Returns:
        dict: 包含电影信息的字典，失败返回 None
    """

    # 1.发送请求，获取电影详情数据
    movie_response = requests.get(movie_info_url, headers=HEADERS, timeout=10)
    print("发送请求{}，获取电影详情成功！".format(movie_info_url))

    # 解析 HTML
    movie_doc = html.fromstring(movie_response.text)

    # 提取各项数据
    movie_names = movie_doc.xpath("//*[@id='content']/h1/span[1]/text()")
    movie_year = movie_doc.xpath("//*[@id='content']/h1/span[2]/text()")

    # 上映日期（提取 YYYY-MM-DD 格式）
    movie_dates = movie_doc.xpath("//*[@id='info']/span[@property='v:initialReleaseDate']/text()")
    movie_dates = re.findall(r'\d{4}-\d{2}-\d{2}', ', '.join(movie_dates)) if movie_dates else []

    # 类型标签
    movie_tags = movie_doc.xpath("//*[@id='info']/span[@property='v:genre']/text()")

    # 片长（提取数字）
    movie_times = movie_doc.xpath('//span[@property="v:runtime"]//text()')
    movie_times = re.findall(r'\d+', ', '.join(movie_times)) if movie_times else []

    # 评分
    movie_score = movie_doc.xpath("//*[@id='interest_sectl']/div[1]/div[2]/strong/text()")

    # 语言
    movie_languages = movie_doc.xpath('//span[text()="语言:"]/following-sibling::text()[1]')

    # 导演
    movie_directors = movie_doc.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')

    # 编剧
    movie_screenwriters = movie_doc.xpath('//*[@id="info"]/span[2]/span[2]/a/text()')

    # 简介（优先获取完整简介，否则获取短简介）
    desc_list = movie_doc.xpath('//span[@class="all hidden"]//text()')
    if not desc_list:
        desc_list = movie_doc.xpath('//span[@property="v:summary"]//text()')

    movie_description = ' '.join(desc_list).replace('\u3000', '').replace('\n', '').replace('\t',
                                                                                            '').strip() if desc_list else ""

    # 组装数据
    movie_info = {
        "电影名": movie_names[0].strip() if movie_names else '',
        "年份": movie_year[0].strip('()') if movie_year else '',
        "上映日期": ",".join(movie_dates) if movie_dates else '',
        "类型": ",".join(movie_tags) if movie_tags else '',
        "片长": movie_times[0].strip() if movie_times else '',
        "评分": movie_score[0].strip() if movie_score else '',
        "语言": movie_languages[0].strip() if movie_languages else '',
        "导演": ",".join(movie_directors) if movie_directors else '',
        "编剧": ",".join(movie_screenwriters) if movie_screenwriters else '',
        "简介": movie_description
    }

    return movie_info


def save_all_movies(all_movies):
    """
    将电影数据保存为 CSV 文件

    Args:
        all_movies: 电影信息字典列表
    """
    with open(MOVIE_LIST_FILE, mode='w', encoding='utf-8-sig', newline='') as csvfile:
        fieldnames = ["电影名", "年份", "上映日期", "类型", "片长", "评分", "语言", "导演", "编剧", "简介"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # 写入表头
        writer.writerows(all_movies)  # 写入电影数据列表

    print(f"✅ 数据保存成功！共 {len(all_movies)} 部电影")
    print(f"📁 文件路径: {MOVIE_LIST_FILE}")


def main():
    """主函数：爬取豆瓣电影 Top250"""

    # 检查 Cookie 是否已配置
    if "请在此处粘贴你的 Cookie" in COOKIE or not COOKIE.strip():
        print("⚠️  警告: 请先在代码中配置你的 Cookie！")
        print("获取方式: 浏览器登录豆瓣 -> F12 -> Network -> 复制 Cookie")

    print("=" * 50)
    print("🎬 豆瓣电影 Top250 爬虫启动")
    print("=" * 50)

    all_movies = []
    total_pages = 1  # 10 页，每页 25 部，共 250 部
    # 遍历每一页
    for page in range(total_pages):
        start = page * 25
        url = f"{DOUBAN_TOP_URL}?start={start}&filter="
        print(f"\n📄 正在爬取第 {page + 1}/{total_pages} 页...")

        # 1. 发送请求（添加请求头）
        response = requests.get(url, headers=HEADERS, timeout=10)
        # 检查请求是否成功
        response.raise_for_status()

        # 2. 解析HTML
        document = html.fromstring(response.text)
        movie_list = document.xpath("//*[@id='content']/div/div[1]/ol/li")
        print("解析HTML，获取电影列表成功！共找到{}部电影".format(len(movie_list)))

        # 3. 遍历电影列表，获取电影详情
        for movie in movie_list:
            movie_urls = movie.xpath(".//div[@class = 'pic']/a/@href")
            if movie_urls:
                movie_info_url = movie_urls[0]
                time.sleep(1)  # 【重要】延时1秒，减轻服务器压力
                # 发送请求，获取电影详情页
                movie_info = get_movie_info(movie_info_url)
                all_movies.append(movie_info)
    save_all_movies(all_movies)
    print("=" * 50)
    print("🏁 爬虫执行完毕")
    print("=" * 50)


if __name__ == '__main__':
    main()