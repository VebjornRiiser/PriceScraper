import requests
import bs4
import time
import datetime
import xml.etree.cElementTree

def getProductList():
    productlist = []
    with requests.get("https://www.komplett.no/sitemap.products.xml") as page:
        if page.status_code == 200:
            soup = bs4.BeautifulSoup(page.text, 'lxml-xml')
            for link in soup.find_all('loc'):
                productlist.append(str(link).strip("</loc>"))
            return productlist
        else:
            print(page.status_code)
            return "error"



def gatherKomplettProductInfo(url):
    try:
        with requests.get(url) as productPage:
            soup = bs4.BeautifulSoup(productPage.text, 'html.parser')
            price = soup.find("span", class_="product-price-now").text
            name =  soup.select_one(".product-main-info-webtext1 > span:nth-child(1)").text
            # print(f"{name} Costs {price}\n{url}\n\n")
            with open(f"prices_komplett_{datetime.date.today()}.txt","a", encoding="utf-8") as file:
                file.write(f"{name};{price};{url}\n")
    except Exception as e:
        with open("errorlog.txt", "a") as errorfile:
            currentTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            errorfile.write(f"{currentTime} : Error when scraping: '{url}' got: {e}\n")
            print(f"{currentTime} : Error when scraping: '{url}' got: {e}")

            # videre funksjoner som burde leggges til:
            # hente ut lastmod fra xml så man slipper å oppdatere alle sidene som ikke har forandret pris
            # hente ut om det kan kjøpes
            # flere sider som kan hentes fra
            # legge inn data i sqlite database


if __name__ == "__main__":
    productlist = getProductList()
    print(f"{len(productlist)} produkter i katalogen til komplett")
    if productlist != "error":
        start = time.time()
        for count, url in enumerate(productlist): # henter alle (ca 18000 10 feb 2021) (ca 14000 1. mars 2022)
            time_used = time.time()-start
            print(f"Framgang: {round(count/len(productlist), 4)}% estimert tid igjen: {round((time_used/(count+1))*(len(productlist)-count+1)/60,1)}m", end="      \r")
            gatherKomplettProductInfo(url)
            time.sleep(0.2) # Waits between each request so that komplett does not block us