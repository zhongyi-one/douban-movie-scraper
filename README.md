# 🎬 豆瓣电影 Top250 爬虫

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-学习项目-orange)]()

> 一个基于 Python + Requests + lxml 的豆瓣电影 Top250 数据爬取工具，仅供学习交流使用。

---

## 📌 项目简介

本项目通过模拟浏览器请求，爬取 [豆瓣电影 Top250](https://movie.douban.com/top250) 榜单中的电影信息，包括：
- 电影名称、年份、上映日期
- 类型、片长、评分
- 导演、编剧、语言
- 剧情简介

数据最终以 **CSV 格式**保存，方便后续数据分析或学习使用。

---

## 🛠️ 技术栈

| 工具/库 | 用途 |
|---------|------|
| `requests` | HTTP 请求 |
| `lxml` | HTML 解析（XPath） |
| `csv` | 数据存储 |
| `re` | 正则表达式提取 |

---

## 📁 项目结构

```
douban-movie-scraper/
├── douban_scraper.py      # 主程序
├── requirements.txt       # 依赖列表
├── .gitignore            # Git 忽略文件
├── LICENSE               # 开源协议
├── README.md             # 项目说明
└── csv_data/             # 数据输出目录
    └── douban_top250_movies.csv
```

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/zhongyi-one/douban-movie-scraper.git
cd douban-movie-scraper
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 Cookie（重要！）

打开 `douban_scraper.py`，找到以下位置：

```python
COOKIE = '''请在此处粘贴你的 Cookie'''
```

**获取 Cookie 的方法：**
1. 浏览器登录 [豆瓣](https://www.douban.com)
2. 按 `F12` 打开开发者工具 → 切换到 **Network** 标签
3. 刷新页面，点击任意一个请求
4. 在右侧 **Headers** 中找到 `Cookie`，复制其值
5. 粘贴到代码中的 `COOKIE` 变量内

### 4. 运行程序

```bash
python douban_scraper.py
```

程序会自动创建 `csv_data/` 目录并保存结果。

---

## ⚙️ 配置参数

在代码顶部可以调整以下参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `total_pages` | `1` | 爬取页数（每页25部，10页共250部） |
| `MOVIE_LIST_FILE` | `./csv_data/...` | 输出文件路径 |

---

## 📊 输出示例

| 电影名 | 年份 | 上映日期 | 类型 | 片长 | 评分 | 语言 | 导演 | 编剧 | 简介 |
|--------|------|----------|------|------|------|------|------|------|------|
| 肖申克的救赎 | 1994 | 1994-09-10 | 犯罪,剧情 | 142 | 9.7 | 英语 | 弗兰克·德拉邦特 | 弗兰克·德拉邦特 | 一场谋杀案使银行家安迪... |

---

## ⚠️ 注意事项

1. **Cookie 有效期**：豆瓣 Cookie 可能会过期，如遇 403 错误请重新获取
2. **请求频率**：默认间隔 1 秒，请勿修改过小以免对服务器造成压力
3. **网络环境**：部分网络可能需要代理才能正常访问豆瓣
4. **反爬机制**：如频繁请求可能导致 IP 被暂时封禁，请合理控制频率
5. **数据更新**：豆瓣页面结构可能变化，如解析失败请检查 XPath 是否需要更新

---

## 📜 免责声明

> **本项目仅供个人学习、研究和技术交流使用，严禁用于任何商业目的。**
>
> 1. 本项目的所有数据来源于 [豆瓣](https://www.douban.com)，版权归豆瓣所有
> 2. 使用者应遵守 [豆瓣使用协议](https://www.douban.com/about?policy=agreement) 及网站的 robots.txt 规则
> 3. 因使用本项目产生的任何法律纠纷或责任，均由使用者自行承担
> 4. 开发者不对因使用本项目导致的账号封禁、IP 限制等后果负责
> 5. 请于下载后 24 小时内删除相关数据，不得传播或用于其他用途

---

## 📚 学习资源

- [Requests 官方文档](https://requests.readthedocs.io/)
- [lxml 文档](https://lxml.de/)
- [XPath 教程](https://www.w3schools.com/xml/xpath_intro.asp)
- [豆瓣](https://www.douban.com/)

---

## 🤝 贡献

欢迎提交 Issue 或 Pull Request！如果是页面结构变化导致的问题，请附上具体的错误信息。

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

---

<p align="center">
  Made with ❤️ for learning purposes only.
</p>
