from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider(RPC_URL))

def get_pair_address(factory_address, token_a, token_b):
    factory_abi = json.loads('[{"constant":true,"inputs":[{"name":"tokenA","type":"address"},{"name":"tokenB","type":"address"}],"name":"getPair","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}]')
    factory = w3.eth.contract(address=factory_address, abi=factory_abi)
    return factory.functions.getPair(token_a, token_b).call()

def get_reserves(pair_address):
    pair_abi = json.loads('[{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"}]')
    pair = w3.eth.contract(address=pair_address, abi=pair_abi)
    reserve0, reserve1, _ = pair.functions.getReserves().call()
    return reserve0, reserve1

def quote_direct_v2_fee(amount_in, reserve_in, reserve_out, fee):
    amount_in_with_fee = amount_in * fee
    numerator = amount_in_with_fee * reserve_out
    denominator = reserve_in + amount_in_with_fee
    return numerator // denominator

def eth_gas_price():
    return w3.eth.gas_price
