from requests_html import HTMLSession
import csv

session = HTMLSession()

def downloadArticlesFromUrl(url):
    print("downloading " + url)
    r = session.get(url)

    # 拿到所有的文章
    searchedArticles = r.html.find('div.r-ent')

    # 整理過的文章集合 [{"title":"title", "url":"url"}]
    articles = []

    for searchedArticle in searchedArticles:
        # 拿到標題相關資訊 title & url
        item = searchedArticle.find('div.title', first=True)

        # 拿 URL, 其中 absolute_links 是 set type, 通過 pop 獲取
        url = item.absolute_links.pop()

        # 拿 title
        title = item.text

        meta = searchedArticle.find('div.meta', first=True)
        author = meta.find('div.author', first=True).text


        # 組合成自己要的格式
        article = {"title": title, "url": url, "author":author}
        articles.append(article)

    with open('output.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
        # 定義欄位
        fieldnames = ['title', 'url', 'author']

        # 將 dictionary 寫入 CSV 檔
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 寫入資料
        for inputArticle in articles:
            writer.writerow(inputArticle)

for page in range(1,1483):
    url = 'https://www.ptt.cc/bbs/Soft_Job/index' + str(page) +'.html'
    downloadArticlesFromUrl(url)