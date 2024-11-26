import requests, time, csv
from bs4 import BeautifulSoup

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = []
    
    for item in soup.select('div.film_cat'):
        title = item.get('data-title', '').strip()
        score = item.get('data-imdb', '').strip()
        genres = item.select_one('.genres')
        link = item.get('data-link', '').strip()
        
        items.append([
            title if title else "N/A",
            score if score else "N/A",
            genres.text.strip() if genres else "N/A",
            link if link else "N/A",
        ])

    return items

def main():
    base_url = "https://filmo.ir/page/{}/?s"
    page = 1
    index = 1

    with open("output.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['شناسه', 'عنوان', 'ژانر', 'امتیاز', 'لینک'])
        
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
