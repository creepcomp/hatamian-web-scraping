import requests
from bs4 import BeautifulSoup
import time
import csv

# Function to scrape items from a page
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = []

    for item in soup.select('div.post-panel-three.search-panel-three'):
        title = item.select_one('div.post-panel-three-bt-info a h4')
        rating = item.select_one('li > a span')
        views = item.select_one('span.post-views-num')
        duration = item.select_one('div.post-panel-three-time a span')
        keywords = ', '.join(kw.text.strip() for kw in item.select('div.post-panel-three-bt-info-end span'))
        link = item.select_one('div.post-panel-three-bt-info a')['href']
        
        items.append([
            title.text.strip() if title else "N/A",
            rating.text.strip() if rating else "N/A",
            views.text.strip() if views else "N/A",
            duration.text.strip() if duration else "N/A",
            keywords if keywords else "N/A",
            link if link else "N/A"
        ])

    return items

def main():
    base_url = "https://peniland.ir/page/{}/?s"
    page = 1
    index = 1

    with open("output.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['شناسه', 'عنوان', 'امتیاز', 'بازدید', 'مدت زمان', 'کلیدواژه ها', 'لینک'])
        
        while True:
            url = base_url.format(page)
            print(url)
            try:
                items = scrape_page(url)
                if not items: break
                for item in items:
                    item = [index] + item
                    writer.writerow(item)
                    index += 1
            except:
                pass
            page += 1
            time.sleep(1)

    print(f"Scraping completed! {index - 1} items were successfully scraped and saved to output.csv")

if __name__ == "__main__":
    main()
