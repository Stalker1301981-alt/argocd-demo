from rpc_v2 import get_pair_address, get_reserves, quote_direct_v2_fee, eth_gas_price
from config import FEE_PANCAKE, FEE_SUSHI, FEE_APE, FEE_BAKERY

def calculate_arbitrage_profit(token_in, token_in_address, token_mid, token_mid_address, amount_in_usd, dexes):
    max_profit = 0
    best_combo = None

    for buy_dex, buy_factory, buy_fee in dexes:
        for sell_dex, sell_factory, sell_fee in dexes:
            if buy_dex == sell_dex:
                continue

            buy_pair = get_pair_address(buy_factory, token_in_address, token_mid_address)
            sell_pair = get_pair_address(sell_factory, token_mid_address, token_in_address)

            reserve_in_buy, reserve_mid_buy = get_reserves(buy_pair)
            reserve_mid_sell, reserve_in_sell = get_reserves(sell_pair)

            amount_mid = quote_direct_v2_fee(
                amount_in_usd * (10 ** 6),
                reserve_in_buy,
                reserve_mid_buy,
                buy_fee
            )

            net_out = quote_direct_v2_fee(
                amount_mid,
                reserve_mid_sell,
                reserve_in_sell,
                sell_fee
            )

            net_out_usd = net_out / (10 ** 6)

            gas_price = eth_gas_price()
            estimated_gas = 200000 * 2
            gas_cost_bnb = (estimated_gas * gas_price) / (10 ** 18)
            bnb_usd_price = 300
            gas_cost_usd = gas_cost_bnb * bnb_usd_price

            net_profit = net_out_usd - amount_in_usd - gas_cost_usd
            profit_pct = (net_profit / amount_in_usd) * 100

            if profit_pct > max_profit and profit_pct >= MIN_PROFIT_PCT:
                max_profit = profit_pct
                best_combo = (buy_dex, sell_dex, net_profit, gas_cost_usd)

    if best_combo:
        buy_dex, sell_dex, net_profit, gas_cost_usd = best_combo
        signal_message = (
            f"✅ АРБИТРАЖНЫЙ СИГНАЛ\n"
            f"Пара: {token_in}/{token_mid}\n"
            f"Объём входа: {amount_in_usd} {token_in}\n"
            f"Покупка на: {buy_dex}\n"
            f"Продажа на: {sell_dex}\n"
            f"Чистая прибыль: {net_profit:.2f} {token_in}\n"
            f"Прибыль (%): {max_profit:.2f}%\n"
            f"Затраты на газ: {gas_cost_usd:.2f} USDT\n"
            f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return signal_message
    else:
        return None
