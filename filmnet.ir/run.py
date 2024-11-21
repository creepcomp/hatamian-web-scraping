import csv, time, requests

COUNT = 40 # (0-40)
DELAY = .5 # Seconds

offset = 0
total = 0

with open("output.csv", 'w') as output:
    csv_writer = csv.writer(output)
    csv_writer.writerow(["عنوان", "عنوان (انگلیسی)", "نوع", "ژانر", "کشور", "سال", "لینک"])
    while True:
        url = f"https://filmnet.ir/api-v2/video-contents?count={COUNT}&offset={offset}"
        response = requests.get(url)
        print(url, response.status_code)
        if response.ok:
            data = response.json()
            items = data["data"]
            if items:
                for item in items:
                    url = "https://filmnet.ir/contents/" + item["short_id"]
                    genre = [x for x in item["categories"] if x["type"] == "genre"]
                    territory = [x for x in item["categories"] if x["type"] == "territory"]
                    item = [
                        item["title"],
                        item["original_name"] if "original_name" in item else "ناموجود",
                        "فیلم" if item["type"] == "single_video" else "سریال",
                        ", ".join([x["title"] for x in genre[0]["items"]]) if genre else "ناموجود",
                        ", ".join([x["title"] for x in territory[0]["items"]]) if territory else "ناموجود",
                        item["year"] if "year" in item else "ناموجود",
                        url
                    ]
                    csv_writer.writerow(item)
                    total += 1
                offset += COUNT
            else:
                break
        time.sleep(DELAY)

print(f"\033[92mProcess completed. (Total: {total})")
