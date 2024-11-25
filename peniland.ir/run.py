import requests
import csv
import time
from bs4 import BeautifulSoup

def extract_movie_info(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    movies = soup.find_all("article", class_="post-film-ind")
    return [
        [
            movie.find("h4").text.strip() if movie.find("h4") else "N/A",
            movie.find("a", href=True)["href"] if movie.find("a", href=True) else "N/A",
            movie.find("li", class_="film-clock-5").find("span").text.strip() if movie.find("li", class_="film-clock-5") else "N/A",
            movie.find("li", class_="film-calendar-alt-regular").find("span").text.strip() if movie.find("li", class_="film-calendar-alt-regular") else "N/A"
        ]
        for movie in movies
    ]

def scrape_movies(output_file):
    base_url = "https://peniland.ir/category/%D8%B3%DB%8C%D9%86%D9%85%D8%A7%DB%8C%DB%8C/page/{}/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

    with open(output_file, "w", encoding="utf-8", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["شناسه", "نام", "زمان", "سال", "لینک"])

        page = 1
        movie_id = 1
        while True:
            url = base_url.format(page)
            print(f"Scraping page: {url}")

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                movie_info = extract_movie_info(response.text)
                if not movie_info:
                    print("No more movies found. Exiting.")
                    break

                for title, link, _time, year in movie_info:
                    csvwriter.writerow([movie_id, title, _time, year, link])
                    movie_id += 1

                page += 1
                time.sleep(1)

            except requests.RequestException as e:
                print(f"Error fetching page {page}: {e}")
                break

if __name__ == "__main__":
    scrape_movies("output.csv")
