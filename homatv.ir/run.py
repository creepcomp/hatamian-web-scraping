import requests, json, re, time, csv

def fetch_videos(pageId: int):
    url = "https://homatv.tv/wp-admin/admin-ajax.php"
    
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,fa;q=0.8",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-requested-with": "XMLHttpRequest"
    }
    
    payload = {
        "action": "loadmore_post",
        "context": "frontend",
        "nonce": "c15adc74ae",  # Update this if necessary
        "query": json.dumps({
            "post_type": "tv_show",
            "posts_per_page": 5,
            "paged": pageId,  # Page number, dynamically updated in the loop
            "orderby": "date ID",
            "order": "DESC",
        }),
        "post_type": "tv_show",
        "box_style": 1,
        "view": "grid",
        "paged": 1
    }
    
    response = requests.post(url, headers=headers, data=payload)
    html_content = response.text
    
    # Regex pattern to extract data
    pattern = re.compile(
        r'post-(?P<index>\d+).*?'
        r'<h3><a href="(?P<url>[^"]+)">(?P<title>[^<]+)</a></h3>.*?'
        r'<span>(?P<genre>[^<]+)</span>',
        re.DOTALL
    )

    # Search for matches
    matches = pattern.finditer(html_content)
    
    return matches

def main():
    with open("output.csv", "w", encoding="utf-8") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(["شناسه", "عنوان", "ژانر", "لینک"])
        page = 1
        while True:
            try:
                items = fetch_videos(page)
                if not items: break
                for item in items:
                    index = item.group("index")
                    title = item.group("title")
                    genre = item.group("genre")
                    url = item.group("url")
                    item = [index, title, genre, url]
                    print(item)
                    csvwriter.writerow(item)
            except: pass
            time.sleep(1)

if __name__ == "__main__":
    main()
