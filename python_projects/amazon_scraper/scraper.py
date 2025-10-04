import json
import random
import time
import requests
from bs4 import BeautifulSoup

# ----------------- CONFIG -----------------
proxies_list = [
    "221.202.27.194:10811",
    "102.68.128.216:8080",
    "154.236.177.104:1976",
    "47.238.128.246:10002",
    "103.85.53.62:8080",
    "181.57.183.26:8080",
    "122.185.198.242:7999",
    "157.15.190.32:8080",
    "45.173.12.141:1994",
    "177.73.186.12:8080",
    "47.91.109.17:45",
    "8.220.136.174:45",
    "8.212.168.170:45",
    "119.93.81.143:8080",
    "8.215.3.250:264",
    "103.81.194.165:8080",
    "47.91.109.17:123",
    "103.156.249.34:8080",
    "104.238.228.201:3128",
    "8.213.215.187:143",
    "175.106.11.172:8080",
    "47.250.177.202:20000",
    "47.90.205.231:33333",
    "67.43.236.22:32923",
    "8.211.51.115:8889",
    "8.215.12.103:8448",
    "118.45.2.136:80",
    "101.200.158.109:8008",
    "47.237.92.86:6379",
    "47.237.92.86:1080",
    "47.237.92.86:1025",
    "47.237.92.86:3129",
    "8.215.12.103:1081",
    "39.102.213.187:8181",
    "8.211.51.115:10000",
    "34.110.150.54:3128",
    "108.35.134.6:5023",
    "103.30.0.249:4145",
    "65.109.92.51:19952",
    "45.249.101.1:56457",
    "41.191.203.163:80",
    "193.31.117.184:80",
    "209.97.150.167:8080",
    "133.18.234.13:80",
    "32.223.6.94:80",
    "190.58.248.86:80",
    "50.122.86.118:80",
    "4.156.78.45:80",
    "107.174.123.200:80",
    "23.247.136.254:80",
    "213.157.6.50:80",
    "201.148.32.162:80",
    "213.33.126.130:80",
    "194.158.203.14:80",
    "189.202.188.149:80",
    "194.219.134.234:80",
    "4.245.123.244:80",
    "92.67.186.210:80",
    "62.171.159.232:8888",
    "102.222.161.143:3128",
    "4.195.16.140:80",
    "124.108.6.20:8085",
    "108.141.130.146:80",
    "20.27.11.248:8561",
    "62.99.138.162:80",
    "103.249.120.207:80",
    "213.143.113.82:80",
    "197.221.234.253:80",
    "185.216.125.251:8888",
    "68.185.57.66:80",
    "127.0.0.7:80",
    "34.160.134.22:3128",
    "123.141.181.24:5031",
    "188.40.57.101:80",
    "192.73.244.36:80",
    "123.141.181.86:5031",
    "116.101.76.85:2076",
    "123.58.219.225:8080",
    "157.250.203.202:8080",
    "34.94.98.68:8080",
    "142.171.224.165:8080",
    "123.141.181.31:5031",
    "154.118.231.30:80",
    "90.162.35.34:80",
    "123.141.181.49:5031",
    "91.103.120.49:443",
    "52.67.251.34:80",
    "115.77.241.248:10001",
    "14.251.13.0:8080",
    "47.254.36.213:123",
    "34.22.184.163:4290",
    "162.240.19.30:80",
    "5.75.196.127:1080",
    "154.65.39.7:80",
    "103.65.237.92:5678",
    "159.192.97.156:4145",
    "38.51.48.85:5678",
    "111.72.128.30:2324",
    "156.228.115.207:3128",
    "45.5.94.150:56731",
    "91.90.114.237:1080",
    "102.177.176.180:80",
    "45.8.211.91:80",
    "166.62.43.174:44889",
    "119.220.241.174:8080",
    "115.76.198.49:24794",
    "104.248.144.71:8080",
    "103.199.97.33:39825",
    "104.21.237.49:80",
    "172.64.146.53:80",
    "23.227.38.135:80",
    "103.79.96.190:4153",
    "41.79.10.218:4673",
    "172.64.87.228:80",
    "45.12.30.111:80",
    "119.82.251.250:48603",
    "45.67.215.156:80",
    "216.205.52.230:80",
    "50.96.204.3:18351",
    "103.79.96.205:4153",
    "23.227.39.249:80",
    "117.74.127.22:1133",
    "218.1.142.61:57114",
    "147.45.40.134:31012",
    "27.68.170.60:1080",
    "89.39.105.228:11423",
    "68.55.186.151:80",
    "185.162.230.55:80",
    "104.19.35.149:80"
]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"
]

# ----------------- helpers -----------------
def make_headers():
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.9", "en-IN,en;q=0.9"]),
        "Connection": "keep-alive",
    }

def proxy_dict(proxy_url):
    if not proxy_url.startswith("http"):
        proxy_url = "http://" + proxy_url
    return {"http": proxy_url, "https": proxy_url}

# Try proxies until we find a response that contains product cards
def get_soup_with_product_check(url, max_attempts=80, delay_between_attempts=0):
    tried = set()
    attempt = 0
    while attempt < max_attempts and len(tried) < len(proxies_list):
        attempt += 1
        proxy_choice = random.choice([p for p in proxies_list if p not in tried])
        tried.add(proxy_choice)
        headers = make_headers()
        try:
            print(f"[Attempt {attempt}] fetching with proxy {proxy_choice} ...")
            resp = requests.get(url, headers=headers, proxies=proxy_dict(proxy_choice), timeout=12)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")

            # Check for product containers
            products = soup.find_all("div", {"cel_widget_id": lambda x: x and x.startswith("MAIN-SEARCH_RESULTS")})
            if products and len(products) > 0:
                print(f"Found {len(products)} product card(s) using proxy {proxy_choice}")
                return soup  # success
            else:
                # no product cards found — treat as a failed attempt and continue trying proxies
                print(f"No product cards found using proxy {proxy_choice}. Trying another proxy...")
                time.sleep(delay_between_attempts)
                continue

        except Exception as e:
            print(f"Request failed with proxy {proxy_choice}: {e}")
            time.sleep(delay_between_attempts)
            continue

    print("All attempts failed — no product cards found.")
    return None

# ----------------- scraping (title + price only) -----------------
def scrape_amazon_prices(url):
    soup = get_soup_with_product_check(url)
    if not soup:
        return None

    products_data = []
    products = soup.find_all("div", {"cel_widget_id": lambda x: x and x.startswith("MAIN-SEARCH_RESULTS")})

    for product in products:
        try:
            title_tag = product.find("h2", class_="a-size-base-plus")
            title = title_tag.get_text(strip=True) if title_tag else None

            price_whole_tag = product.find("span", class_="a-price-whole")
            price_fraction_tag = product.find("span", class_="a-price-fraction")
            if price_whole_tag:
                price = price_whole_tag.get_text(strip=True) + (price_fraction_tag.get_text(strip=True) if price_fraction_tag else "")
            else:
                price = None
            if title:
                products_data.append({
                    "title": title,
                    "price": price
                })

        except Exception as e:
            print("Error parsing a product card:", e)

    return products_data

# ----------------- save history -----------------
def save_price_history(entry, filename="prices_history.json"):
    import os

    # If file doesn't exist or is empty, start with empty list
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        history = []
    else:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            # File corrupted or empty, start fresh
            history = []

    history.append(entry)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

# ----------------- main -----------------
if __name__ == "__main__":
    url = "https://www.amazon.in/s?k=nike+sneakers"
    scraped = scrape_amazon_prices(url)

    if not scraped:
        print("Scrape failed: no product data could be retrieved this run.")
    else:
        # create dated entry and append to JSON
        today = time.strftime("%Y-%m-%d")
        entry = {"date": today, "products": scraped}
        save_price_history(entry)
        print(f"Saved {len(scraped)} product records for {today} to prices_history.json")
