import time
import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config import *
from arbitrage import calculate_arbitrage_profit
import requests

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Telegram error: {response.text}")
    except Exception as e:
        print(f"Send error: {e}")

def main():
    print("Arbitrage bot started on BSC")
    print(f"Pairs: {[pair[0] + '/' + pair[2] for pair in WATCHLIST]}")

    dexes = [
        ("Sushi", SUSHI_FACTORY_V2, FEE_SUSHI),
        ("PancakeSwap", PANCAKE_FACTORY_V2, FEE_PANCAKE),
        ("ApeSwap", APE_FACTORY_V2, FEE_APE),
        ("BakerySwap", BAKERY_FACTORY_V2, FEE_BAKERY)
    ]

    while True:
        for token_in, token_in_address, token_mid, token_mid_address in WATCHLIST:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Checking {token_in}/{token_mid}...")
            signal = calculate_arbitrage_profit(
                token_in, token_in_address, token_mid, token_mid_address,
                AMOUNT_USDT, dexes
            )
            if signal:
                print("ARBITRAGE FOUND!")
                print(signal)
                send_telegram_message(signal)
            else:
                print(f"No profit for {token_in}/{token_mid}")

        time.sleep(SCAN_INTERVAL_SEC)

if __name__ == "__main__":
    main()
