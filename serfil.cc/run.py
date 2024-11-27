import requests, csv, time
from bs4 import BeautifulSoup

OUTPUT = "output.csv"

TYPES = [
    "movies",
    "series"
]

GENRES = [
    "آهنگ",
    "اکشن",
    "انیمیشن",
    "بزرگسال",
    "بیوگرافی",
    "تاریخی",
    "ترسناک",
    "جنایی",
    "جنگی",
    "خانوادگی",
    "درام",
    "رازآلود",
    "عاشقانه",
    "علمی تخیلی",
    "فانتزی",
    "فیلم نوآر",
    "کمدی",
    "کوتاه",
    "ماجراجویی",
    "مستند",
    "موزیکال",
    "هیجان انگیز",
    "ورزشی",
    "وسترن"
]

def scrape_page(type, genre, page):
    url = f"https://serfil.cc?ad-s=1&type={type}&genr={genre}&page={page}"
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.select("section.stream-posts article.post-item")
    items = []
    for post in posts:
        title = post.select_one("div.title-box h2")
        imdb_rate = post.select_one("div.imdb-rate span")
        popular_rate = post.select_one("div.popular-rate span")
        link = post.select_one("a.item")
        items.append([
            title.text.strip() if title else "N/A",
            imdb_rate.text.strip() if imdb_rate else "N/A",
            popular_rate.text.strip() if popular_rate else "N/A",
            link["href"] if link else "N/A",
        ])
    return items

def main():
    index = 1
    with open(OUTPUT, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["شناسه", "عنوان", "نوع", "ژانر", "امتیاز", "محبوبیت", "لینک"])
        for type in TYPES:
            for genre in GENRES:
                page = 1
                while True:
                    try:
                        items = scrape_page(type, genre, page)
                        if not items: break
                        for item in items:
                            item = [index] + item
                            writer.writerow(item)
                            print(item)
                            index += 1
                        page += 1
                    except: pass
                    time.sleep(1)
    
    print(f"Scraping completed! {index - 1} items were successfully scraped and saved to output.csv")

if __name__ == "__main__":
    main()
