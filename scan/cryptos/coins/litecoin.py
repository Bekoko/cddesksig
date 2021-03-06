from .base import BaseCoin
from ..explorers import blockcypher

class Litecoin(BaseCoin):
    coin_symbol = "ltc"
    display_name = "Litecoin"
    segwit_supported = True
    magicbyte = 48
    #script_magicbyte = 50 #Supposed to be new magicbyte
    script_magicbyte = 5 #Old magicbyte still recognised by explorers
    explorer = blockcypher
    # testnet_overrides = {
    #     'display_name': "Litecoin Testnet",
    #     'coin_symbol': "LTCTEST",
    #     'magicbyte': 111,
    #     #script_magicbyte: 58   #Supposed to be new magicbyte
    #     'script_magicbyte': 196 #Old magicbyte still recognised by explorers
    # }
