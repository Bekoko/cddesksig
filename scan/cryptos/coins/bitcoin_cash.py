from .base import BaseCoin
from ..transaction import SIGHASH_ALL, SIGHASH_FORKID
from ..explorers import restbitcoin

class BitcoinCash(BaseCoin):
    coin_symbol = "BCH"
    display_name = "Bitcoin Cash"
    segwit_supported = False
    magicbyte = 0
    script_magicbyte = 5
    explorer = restbitcoin
    hashcode = SIGHASH_ALL + SIGHASH_FORKID
    # testnet_overrides = {
    #     'display_name': "Bitcoin Cash Testnet",
    #     'coin_symbol': "tbcc",
    #     'magicbyte': 111,
    #     'script_magicbyte': 196
    # }