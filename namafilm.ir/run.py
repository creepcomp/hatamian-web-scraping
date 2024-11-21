import requests, re, csv, time

def get_video_items(pageId: int):
    # GraphQL API URL
    url = "https://www.namafilm.ir/admin/api.aspx/LoadVideo"

    # Required headers
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,fa;q=0.8",
        "content-type": "application/json; charset=UTF-8",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest"
    }
    
    # Required Post Body such as (PageNumber,)
    data = {
        "VFID": 0,
        "PageNumber": pageId,
        "Key": "nYZoMmcnUcMQQBbeD5nSxm7dpTBaBeLOrHgnQuAa0+AFbmKCq5DwqGEG+ZD2IziQRrvMxtKWdwx5lq8vGyzykQLHhtxfqSincInEg5xE94maTae9ieIuMC8x$S7+rM5uzrwHl53s9VY80Jr5NkeLDFG1frAmSmRJ9D$lu9dzr6Id0I4Ir5qkgGWlO6$52h9QbqDLec8miVdpNCBI$0fBci6OC2HicXCXKl3msjrEv68S$2rgS9AfytWCNgoIWgJnE7ByvBRTP3CHmiZMEI6CMvtPIWB8RLyzCK45fVJQzfxgS4wVxAE6n2qHQ5yfcoP7j9LVNYpynmVfleQ2WZHvuSID8fAxgdOQsNj6X8d$Ra0apt7uXeC8Ejg7D02cAs1OE7m42I6egCMY+DIjbG4GWA==",
        "wid": "1"
    }
    
    # Fetch & Clean Data
    response = requests.post(url, headers=headers, json=data, cookies=None)
    data = response.json()
    data = data['d']
    html_content = data.lstrip("1╬") # Clean HTML Content
    
    # Regular expression to extract the necessary data
    pattern = re.compile("".join([
        r"<div class='VideoItem '>.*?",
        r"<a class=\"item Fade\" href='([^']+)'>",      # Extract URL
        r".*?",
        r"<div class=\"viCat viCat2\">(\d{4})</div>",   # Extract year
        r".*?",
        r"<div class=\"VTTitle Fade\">([^<]+)</div>",   # Extract title
        r"</a>",
        r"</div>"
    ]))

    # Finding all matches
    matches = pattern.findall(html_content)
    
    return matches

def main():
    with open("output.csv", 'w', encoding="utf-8") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(["شناسه", "عنوان", "سال", "لینک"])
        pageId = 1
        while True:
            try:
                items = get_video_items(pageId)
                if not items: break
                for url, year, title in items:
                    item = [url.split('/')[-1], title, year, url]
                    csvwriter.writerow(item)
                    print(item)
                pageId += 1
                time.sleep(1)
            except:
                pass

if __name__ == "__main__":
    main()
