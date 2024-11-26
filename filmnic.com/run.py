import requests
import csv
import json
import time

TOKEN = "token a1da490f2a2bd6e:5cd286e5e20d146"
LENGTH = 1000

def main():
    start = 0
    index = 0
    with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["شناسه", "عنوان", "دسته", "ژانر", "لینک"])

        while True:
            try:
                response = requests.post(
                    "https://filmnic.com/api/method/frappe.desk.reportview.get",
                    headers={"Authorization": TOKEN},
                    json={"doctype": "Movie", "fields": ["name", "title", "is_serial", "information_json"], "start": start, "page_length": LENGTH}
                )
                data = response.json()
                if not data["message"]: break
                items = data.get("message", {}).get("values", [])

                for item in items:
                    name, title, is_serial, information_json = item
                    genre = ", ".join(json.loads(information_json).get("genre", [])) if information_json else "N/A"
                    link = f"https://filmnic.com/serial/{name}" if is_serial == "1" else f"https://filmnic.com/movie/{name}"
                    item = [index, title, "سریال" if is_serial == "1" else "فیلم", genre, link]
                    writer.writerow(item)
                    print(item)
                    index += 1
                
                start += LENGTH
            except:
                pass
            
            time.sleep(1)

    print(f"Scraping complete! A total of {index} items have been successfully saved to 'output.csv'.")

if __name__ == "__main__":
    main()
