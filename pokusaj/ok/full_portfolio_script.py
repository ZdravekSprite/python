import os
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

# -----------------------------
# CONFIG
# -----------------------------
load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET") or ""
BASE_URL = "https://api.binance.com"

# -----------------------------
# HELPER: Signed Request
# -----------------------------
def get_server_time():
    url = BASE_URL + "/api/v3/time"
    r = requests.get(url)
    return int(r.json()["serverTime"])

def signed_request(http_method, url_path, payload={}):
    payload['timestamp'] = get_server_time()
    query_string = urlencode(payload)
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    query_string += f"&signature={signature}"
    headers = {"X-MBX-APIKEY": API_KEY}

    if http_method == "GET":
        response = requests.get(BASE_URL + url_path, headers=headers, params=query_string)
    elif http_method == "POST":
        response = requests.post(BASE_URL + url_path, headers=headers, params=query_string)
    else:
        raise ValueError("Unsupported HTTP method")
    
    return response.json()

# -----------------------------
# HELPER: Convert asset to EUR
# -----------------------------
def get_eur_value(asset, amount):
    if amount == 0:
        return 0
    if asset == "EUR":
        return amount
    if asset == "USDT":
        # Convert USDT → EUR
        price = float(requests.get(BASE_URL + "/api/v3/ticker/price", params={"symbol": "EURUSDT"}).json()["price"])
        return amount / price
    if asset == "USDC":
        # Convert USDC → EUR
        price = float(requests.get(BASE_URL + "/api/v3/ticker/price", params={"symbol": "EURUSDC"}).json()["price"])
        return amount / price
    symbol = asset + "EUR"
    try:
        price = float(requests.get(BASE_URL + "/api/v3/ticker/price", params={"symbol": symbol}).json()["price"])
        return amount * price
    except:
        return 0  # No EUR pair available

# -----------------------------
# SPOT WALLET
# -----------------------------
def get_spot_portfolio():
    print("\n===== SPOT WALLET =====")
    data = signed_request("GET", "/api/v3/account")
    total_value = 0
    for b in data['balances']:
        if b["asset"][:2] == "LD":
            continue  # Skip locked assets
        asset = b["asset"]
        free = float(b["free"])
        locked = float(b["locked"])
        total = free + locked
        if total > 0:
            eur_val = get_eur_value(asset, total)
            total_value += eur_val
            print(f"{asset}: {total:.8f} (~{eur_val:.2f} €)")
    return total_value

# -----------------------------
# FLEXIBLE EARN POSITIONS
# -----------------------------
def get_flexible_earn_positions():
    print("\n===== FLEXIBLE EARN POSITIONS =====")
    try:
        data = signed_request("GET", "/sapi/v1/simple-earn/flexible/position")
    except Exception as e:
        print("→ Cannot fetch Flexible Earn positions:", e)
        return 0

    total_value = 0
    for p in data.get("rows", []):
        asset = p["asset"]
        amount = float(p["totalAmount"])
        eur_val = get_eur_value(asset, amount)
        apr = float(p.get("latestAnnualPercentageRate", 0)) * 100
        rewards = float(p.get("cumulativeTotalRewards", 0))
        total_value += eur_val
        #print(f"{asset}: deposited={amount} (~{eur_val:.2f} €)")
        print(f"{asset}: {amount} (~{eur_val:.2f} €), APR={apr:.2f}%, rewards={rewards}")
    print(f"TOTAL FLEXIBLE EARN VALUE: {total_value:.2f} €")
    return total_value

# -----------------------------
# SPOT OPEN ORDERS
# -----------------------------
def get_spot_open_orders():
    print("\n===== SPOT OPEN ORDERS =====")

    try:
        orders = signed_request("GET", "/api/v3/openOrders")
    except Exception as e:
        print("→ Cannot fetch spot open orders:", e)
        return

    if not orders:
        print("No open spot orders.")
        return

    for o in orders:
        symbol = o["symbol"]
        side = o["side"]
        otype = o["type"]
        qty = float(o["origQty"])
        price = float(o["price"])
        ts = o["time"]
        time_placed = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts / 1000))

        #print(f"\n--- {symbol} ---")
        #print(f"Side: {side}")
        #print(f"Type: {otype}")
        #print(f"Quantity: {qty}")
        now_price = float(requests.get(BASE_URL + "/api/v3/ticker/price", params={"symbol": symbol}).json()["price"])
        print(f"{symbol} {side} {qty} Price: {price} ({now_price} {(1 - price/now_price if symbol == "SELL" else price/now_price - 1)*100:.2f}%)")
        #print(f"Status: {o['status']}")
        #print(f"Order Time: {time_placed}")
        #print(f"Time In Force: {o['timeInForce']}")
        #print(f"Client Order ID: {o['clientOrderId']}")

# -----------------------------
# RUN EVERYTHING
# -----------------------------
if __name__ == "__main__":
    #'''
    total_portfolio = 0
    total_portfolio += get_spot_portfolio()
    time.sleep(0.2)
    total_portfolio += get_flexible_earn_positions()

    print("\n=======================================")
    print(f"TOTAL PORTFOLIO VALUE: {total_portfolio:.2f} €")
    print("=======================================")

    #'''
    # New: print Spot open orders
    get_spot_open_orders()

    print("=======================================\n")