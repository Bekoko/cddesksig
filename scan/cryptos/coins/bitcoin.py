from ..explorers import blockcypher
from .base import BaseCoin


class Bitcoin(BaseCoin):
    coin_symbol = "btc"
    display_name = "Bitcoin"
    segwit_supported = True
    magicbyte = 0
    script_magicbyte = 5
    explorer = blockcypher
    testnet_overrides = {
        'display_name': "Bitcoin Testnet",
        'coin_symbol': "btc-testnet",
        'magicbyte': 111,
        'script_magicbyte': 196
    }