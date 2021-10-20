from . import base_insight as insight
import re
import requests

# def get_url(coin_symbol):
#     if coin_symbol == "DASH":
#         return "https://insight.dash.siampm.com/api"
#     return "https://test.insight.dash.siampm.com/api"
base_url = "https://insight.dashevo.org/insight/"
address_url = base_url + "address/%s" #address
# sendtx_url = base_url + "v2/rawtransactions/sendRawTransaction/%s" # tx
# utxo_url = base_url + "v2/address/utxo/%s"#address

def history(addr, coin_symbol="DASH"):
    url = address_url % (addr)
    response = requests.get(url)
    return response.json()

def unspent(addr, coin_symbol="DASH"):
    url = utxo_url % (addr)
    response = requests.get(url)
    return response.json()

def pushtx(tx, coin_symbol="DASH"):
    if not re.match('^[0-9a-fA-F]*$', tx):
        tx = tx.encode('hex')
    url = sendtx_url % (tx)
    response = requests.get(url)
    return response.json()


# # def history(*args,  coin_symbol="DASH"):
# #     base_url = get_url(coin_symbol)
# #     return insight.history(base_url, *args)


# # def unspent(*args, coin_symbol="DASH"):
# #     base_url = get_url(coin_symbol)
# #     return insight.unspent(base_url, *args)

# def fetchtx(txhash, coin_symbol="DASH"):
#     base_url = get_url(coin_symbol)
#     return insight.fetchtx(base_url, txhash)

# def txinputs(txhash, coin_symbol="DASH"):
#     base_url = get_url(coin_symbol)
#     return insight.txinputs(base_url, txhash)

# # def pushtx(tx, coin_symbol="DASH"):
# #     base_url = get_url(coin_symbol)
# #     return insight.pushtx(base_url, coin_symbol, tx)

# def block_height(tx, coin_symbol="DASH"):
#     base_url = get_url(coin_symbol)
#     return insight.block_height(base_url, tx)

# def current_block_height(coin_symbol="DASH"):
#     base_url = get_url(coin_symbol)
#     return insight.current_block_height(base_url)

# def block_info(height, coin_symbol="DASH"):
#     base_url = get_url(coin_symbol)
#     return insight.block_info(base_url, height)