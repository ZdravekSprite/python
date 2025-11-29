# pip install websockets aiohttp python-dotenv colorama
# binance_dashboard.py

import asyncio
import websockets
import json
import time
import aiohttp
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv
from collections import deque
from datetime import datetime
from typing import Dict, List, Deque, Optional, Mapping
from colorama import Fore, Style, init

init(autoreset=True)
load_dotenv()

# ----------------------------- CONFIG ---------------------------------

SYMBOLS: List[str] = ["btcusdc", "ethusdc", "bnbusdc", "solusdc"]
symbol_streams = "/".join(f"{s}@trade" for s in SYMBOLS)
BINANCE_WS_URL = f"wss://stream.binance.com:9443/stream?streams={symbol_streams}"

FPS = 1
REDRAW_INTERVAL = 1.0 / FPS
HISTORY_LEN = 45
SPARK = "▁▂▃▄▅▆▇█"

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = (os.getenv("BINANCE_API_SECRET") or "").encode()
API_URL = "https://api.binance.com"

# ----------------------------------------------------------------------


def make_sparkline(values: List[float]) -> str:
    if len(values) < 2:
        return "....."
    mn, mx = min(values), max(values)
    if mx - mn == 0:
        return "─" * len(values)
    chars = []
    for v in values:
        idx = int((v - mn) / (mx - mn) * (len(SPARK) - 1))
        chars.append(SPARK[idx])
    return "".join(chars)


# --------------------------- BINANCE API --------------------------------

async def signed_request(method: str, path: str, params: dict = {}):
    if params is None:
        params = {}

    params["timestamp"] = int(time.time() * 1000)
    query = urlencode(params)

    signature = hmac.new(API_SECRET, query.encode(), hashlib.sha256).hexdigest()
    url = f"{API_URL}{path}?{query}&signature={signature}"

    headers = {"X-MBX-APIKEY": API_KEY or ""}

    async with aiohttp.ClientSession() as session:
        if method == "GET":
            async with session.get(url, headers=headers) as resp:
                return await resp.json()
        else:
            async with session.post(url, headers=headers) as resp:
                return await resp.json()


async def get_account_balances():
    data = await signed_request("GET", "/api/v3/account")
    return {
        asset["asset"]: float(asset["free"]) + float(asset["locked"])
        for asset in data["balances"]
        if float(asset["free"]) + float(asset["locked"]) > 0
    }


async def get_open_orders():
    return await signed_request("GET", "/api/v3/openOrders")


async def get_portfolio_value(prices: Mapping[str, Optional[float]]):
    balances = await get_account_balances()
    total = 0.0

    for asset, amount in balances.items():
        pair = asset.lower() + "usdc"
        if asset == "USDC":
            total += amount
        else:
            price = prices.get(pair)
            if price is not None:
                total += amount * price

    return total, balances


# ---------------------- WEBSOCKET DASHBOARD -----------------------------


async def connect_and_listen():
    prev_price: Dict[str, Optional[float]] = {s: None for s in SYMBOLS}
    latest_price: Dict[str, Optional[float]] = {s: None for s in SYMBOLS}
    history: Dict[str, Deque[float]] = {s: deque(maxlen=HISTORY_LEN) for s in SYMBOLS}

    balances = {}
    open_orders = []
    portfolio_value = 0.0
    last_redraw = 0.0
    last_account_update = 0.0

    while True:
        try:
            async with websockets.connect(BINANCE_WS_URL) as ws:
                print("Connected to Binance WebSocket")

                async for raw_msg in ws:
                    msg = json.loads(raw_msg)
                    data = msg["data"]
                    stream = msg["stream"]
                    symbol = stream.split("@")[0]

                    price = float(data["p"])
                    latest_price[symbol] = price
                    history[symbol].append(price)

                    now = time.time()

                    # Update account every 10 sec
                    if now - last_account_update > 10:
                        try:
                            portfolio_value, balances = await get_portfolio_value(latest_price)
                            open_orders = await get_open_orders()
                        except Exception as e:
                            print("Account update error:", e)
                        last_account_update = now

                    if now - last_redraw < REDRAW_INTERVAL:
                        continue
                    last_redraw = now

                    # Clear terminal
                    print("\033[H\033[J", end="")
                    print(f"┌────────── Binance Live Prices (Last {HISTORY_LEN} Trades) ─────────────────────────┐")

                    for s in SYMBOLS:
                        current = latest_price[s]
                        prev = prev_price[s]

                        if current is None:
                            print(f" {s.upper():10} waiting...")
                            continue

                        if prev is None:
                            color, arrow = Fore.WHITE, "-"
                        elif current > prev:
                            color, arrow = Fore.GREEN, "↑"
                        elif current < prev:
                            color, arrow = Fore.RED, "↓"
                        else:
                            color, arrow = Fore.WHITE, "-"

                        spark = make_sparkline(list(history[s]))

                        print(
                            f" {color}{s.upper():10} {current:<12} {arrow}  "
                            f"{spark}{Style.RESET_ALL}"
                        )

                    print("└─────────────────────────────────────────────────────────────────────────┘")

                    # ---- ACCOUNT SECTION ----
                    print("\n┌────────── Account Summary ───────────────────────────────────────────────┐")
                    for asset, amt in balances.items():
                        print(f" {asset:6}: {amt}")
                    print(f"\n Open Orders: {len(open_orders)}")
                    print(f" Portfolio Value: {portfolio_value:.2f} USDC")
                    print("└──────────────────────────────────────────────────────────────────────────┘")

                    print("Updated:", datetime.now().strftime("%H:%M:%S"))

                    prev_price[symbol] = price

        except Exception as e:
            print(f"Error: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(connect_and_listen())
