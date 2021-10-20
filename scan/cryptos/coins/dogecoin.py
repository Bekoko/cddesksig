from .base import BaseCoin
from ..explorers import blockcypher


class Doge(BaseCoin):
    coin_symbol = "doge"
    display_name = "Dogecoin"
    segwit_supported = False
    magicbyte = 30
    explorer = blockcypher
    # testnet_overrides = {
    #     'display_name': "Dogecoin Testnet",
    #     'coin_symbol': "Dogecoin",
    #     'magicbyte': 113,
    # }