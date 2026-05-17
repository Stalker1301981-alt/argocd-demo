from src.config import *

def test_config_has_rpc_url():
    assert RPC_URL.startswith("https://")

def test_config_has_watchlist():
    assert len(WATCHLIST) > 0

def test_config_has_dexes():
    assert PANCAKE_FACTORY_V2.startswith("0x")
    assert SUSHI_FACTORY_V2.startswith("0x")

def test_config_amount_positive():
    assert AMOUNT_USDT > 0

def test_config_scan_interval_positive():
    assert SCAN_INTERVAL_SEC > 0
