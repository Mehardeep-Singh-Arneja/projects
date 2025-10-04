import json
import os
import matplotlib.pyplot as plt
import numpy as np

# ----------------- Load history -----------------
filename = "prices_history.json"
if not os.path.exists(filename):
    print(f"{filename} not found!")
    exit()

with open(filename, "r", encoding="utf-8") as f:
    try:
        history_data = json.load(f)
    except json.JSONDecodeError:
        print(f"{filename} is empty or corrupted!")
        exit()

if not history_data:
    print("No historical data found.")
    exit()

# ----------------- Aggregate prices -----------------
price_history = {}
all_dates = set()

for entry in history_data:
    date = entry.get("date", "unknown_date")
    all_dates.add(date)
    products = entry.get("products", [])

    for product in products:
        title = product.get("title") or "Unknown Product"
        price_str = product.get("price") or "0"

        try:
            price_val = float(price_str.replace(",", "").replace("₹", "").strip())
        except:
            price_val = None

        if title not in price_history:
            price_history[title] = {}
        price_history[title][date] = price_val

sorted_dates = sorted(all_dates)
product_titles = list(price_history.keys())

# ----------------- Prepare 3D data -----------------
X = []  # date indices
Y = []  # price
Z = []  # product indices

for zi, title in enumerate(product_titles):
    product_data = price_history[title]
    last_price = None
    for xi, d in enumerate(sorted_dates):
        if d in product_data and product_data[d] is not None:
            last_price = product_data[d]
        # forward fill last known price
        price = last_price if last_price is not None else 0
        X.append(xi)
        Y.append(price)
        Z.append(zi)


fig = plt.figure(figsize=(18, 10))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(X, Y, Z, c=Y, cmap='viridis', depthshade=True)

ax.set_xticks(range(len(sorted_dates)))
ax.set_xticklabels(sorted_dates, rotation=45, ha='right')
ax.set_yticks(np.arange(0, max(Y)+1000, step=1000))
ax.set_zticks(range(len(product_titles)))
ax.set_zticklabels(product_titles)

ax.set_xlabel("Date")
ax.set_ylabel("Price (₹)")
ax.set_zlabel("Product")

plt.title("3D Price History of Products Over Time")
plt.tight_layout()
plt.show()
