import requests, re, csv

def extract_content_data(html):
    pattern = re.compile(
        r'<a href="(?P<url>https://filmaland\.ir/(movies|series)/\d+)".*?alt="(?P<title>.*?)\s\((?P<year>\d{4})\)"',
        re.DOTALL
    )
    matches = pattern.findall(html)
    content = [
        {
            "type": "سریال" if "series" in m[0] else "فیلم",
            "url": m[0],
            "title": m[2],
            "year": m[3]
        }
        for m in matches
    ]
    return content

def main():
    response = requests.get("https://filmaland.ir/search")
    items = extract_content_data(response.text)
    with open("output.csv", 'w', encoding='utf-8') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(["شناسه", "عنوان", "نوع", "سال", "لینک"])
        for index, item in enumerate(items):
            print([index, item["title"], item["type"], item["year"], item["url"]])
            csvwriter.writerow([index, item["title"], item["type"], item["year"], item["url"]])

if __name__ == "__main__":
    main()
