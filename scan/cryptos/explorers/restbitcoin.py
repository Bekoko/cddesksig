import re
import requests

# https://developer.bitcoin.com/rest/docs/rawtransactions

base_url = "https://rest.bitcoin.com/"
sendtx_url = base_url + "v2/rawtransactions/sendRawTransaction/%s" # tx
address_url = base_url + "v2/address/details/%s" #address
utxo_url = base_url + "v2/address/utxo/%s"#address

def history(addr, coin_symbol="BCH"):
    url = address_url % (addr)
    response = requests.get(url)
    return response.json()

def unspent(addr, coin_symbol="BCH"):
    url = utxo_url % (addr)
    response = requests.get(url)
    return response.json()

def pushtx(tx, coin_symbol="BCH"):
    if not re.match('^[0-9a-fA-F]*$', tx):
        tx = tx.encode('hex')
    url = sendtx_url % (tx)
    response = requests.get(url)
    return response.json()
