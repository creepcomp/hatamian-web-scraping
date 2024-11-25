import requests, re, csv

def get_series():
    # Get Html Content by GET Request.
    response = requests.get("https://toonyland.ir/english-collection")
    html_content = response.text
    
    # Regex pattern to extract details
    pattern = r'<a href="([^"]+)"[^>]*?class="masvideos-LoopTvShow-link[^"]*".*?<h3[^>]*?class="[^"]*tv-show__title[^"]*">(.*?)</h3>.*?"'

    # Extract matches
    matches = re.findall(pattern, html_content, re.DOTALL)
    matches = list(set(matches))
    
    matches = [[link, title, "سریال"] for link, title in matches]
    
    return matches

def get_movies():
    # Get Html Content by GET Request.
    response = requests.get("https://toonyland.ir/movie-english")
    html_content = response.text
    
    # Regex pattern to extract details
    pattern = r'<h3[^>]*>\s*<strong>\s*<a\s+href="([^"]+)">(.*?)<\/a>\s*<\/strong>\s*<\/h3>'

    # Extract matches
    matches = re.findall(pattern, html_content, re.DOTALL)
    matches = list(set(matches))
    
    matches = [[link, title, "فیلم"] for link, title in matches]
    
    return matches

def main():
    with open("output.csv", "w", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["شناسه", "نام", "دسته", "لینک"])
        series = get_series()
        movies = get_movies()
        series.extend(movies)
        for index, (link, title, category) in enumerate(series):
            item = [index, title, category, link]
            csvwriter.writerow(item)
            print(item)

if __name__ == "__main__":
    main()