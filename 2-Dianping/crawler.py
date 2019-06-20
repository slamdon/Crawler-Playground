from requests_html import HTMLSession
import csv

session = HTMLSession()
baseUrl = 'https://www.dianping.com'

cities = [
    'kaohsiung', 'Hengchun', 'hualien', 'keelung', 'chiayi',
    'kenting', 'miaoli', 'riyuetan', 'penghu', 'taipei', 'taitung',
    'tainan', 'taiwan', 'taichung', 'taoyuan', 'newtaipei', 'hsinchu', 'ilan', 'zhanghua'
]


def downloadFromUrl(baseUrl, page):
    url = baseUrl + str(page)
    print("downloading " + url)
    response = session.get(url)

    # 拿到所有的店家
    searchedItems = response.html.find('#searchList')

    shops = []

    for searchedItem in searchedItems:
        # 拿到 shopname & address
        items = searchedItem.find('ul.detail')

        for item in items:
            name = ''
            address = ''
            tel = ''

            name = item.find('li.shopname a', first=True).attrs['title']
            addressTel = item.find('li.address', first=True).text
            addressTel = addressTel.split('\xa0\xa0')
            if len(addressTel) == 1:
                address = addressTel[0]
            elif len(addressTel) == 2:
                address = addressTel[0]
                tel = addressTel[1]

            shop = {"name": name, "address": address, "tel": tel}
            shops.append(shop)

    with open('output.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
        # 定義欄位
        fieldnames = ['name', 'address', 'tel']

        # 將 dictionary 寫入 CSV 檔
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 寫入資料
        for shop in shops:
            writer.writerow(shop)


    # 頁數
    nextPage = response.html.find('a.NextPage', first=True)

    if(type(nextPage) == 'NoneType'):
        print('has no next page')
    
    if(nextPage != None):
        nextPage = nextPage.attrs['data-ga-page']
        downloadFromUrl(baseUrl, nextPage)

def downloadFromCity(cityName, category):
    downloadUrl = baseUrl + '/' + cityName + '/' + category + '/p'
    downloadFromUrl(downloadUrl, 1)

for city in cities:
    downloadFromCity(city, 'food')

