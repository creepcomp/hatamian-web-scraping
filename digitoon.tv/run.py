import requests, csv, time

def get_categories():
    response = requests.get("https://www.digitoon.tv/_next/data/vRSntz6GRfRxkNnUuk8a8/category.json")
    data = response.json()
    return data["pageProps"]["categories"]

def get_category_products(id):
    response = requests.get(f"https://apitwo.digitoon.ir/api/v3/web/product-list/{id}/?limit=100000")
    data = response.json()
    return data["products"]

def main():
    with open("digitoon.csv", "w", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["شناسه", "نام", "نام انگلیسی", "دسته بندی", "لینک"])
        categories = get_categories()
        for category in categories:
            print(f"https://www.digitoon.tv/category/{category["id"]}")
            products = get_category_products(category["id"])
            for product in products:
                print(f"https://www.digitoon.tv/animations/{product["id"]}")
                csvwriter.writerow([product["id"], product["name"], product["name_english"], category["title"], f"https://www.digitoon.tv/animations/{product["id"]}"])
            time.sleep(1)

if __name__ == "__main__":
    main()
