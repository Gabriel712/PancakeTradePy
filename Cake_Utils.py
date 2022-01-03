import requests
import json
from web3 import Web3
import time

def get_price(token):
    url = f"https://api.pancakeswap.info/api/v2/tokens/{token}"
    return(float(json.loads(requests.get(url).text)["data"]["price"]))


def get_status_transaction(txnHash):
    bsc = "https://bsc-dataseed.binance.org/"
    web3 = Web3(Web3.HTTPProvider(bsc))
    block = web3.eth.getTransactionReceipt(txnHash)
    response = {"status":block["status"], "gasUsed":block["gasUsed"], "txnHash":txnHash}
    return(response)
    #print(get_status_transaction("0x21c6bc95f7d3b638663b1d3a3a3226b4603fcc7b82dfd00ed80dc88284dc05d6"))
    #error = indexing / response['status'] = 0 FAIL / response['status'] = 1 SUCCESS

def sniper_token(token_buy_address, buy_when):
    x = round(get_price(token_buy_address),2)
    while x != buy_when:
        time.sleep(1)
        x = round(get_price(token_buy_address),2)
    if x == buy_when:
        return(True)

def get_token_amount(token_buy_address, token_address):
    bsc = "https://bsc-dataseed.binance.org/";web3 = Web3(Web3.HTTPProvider(bsc))
    contract_id = web3.toChecksumAddress(token_address)
    sellAbi = open('Pancake_ABI_Sell_Contract.abi', 'r').read()
    sellTokenContract = web3.eth.contract(contract_id, abi=sellAbi)
    balance = sellTokenContract.functions.balanceOf(token_buy_address).call()
    symbol = sellTokenContract.functions.symbol().call()
    readable = web3.fromWei(balance,'ether')
    readable = round(float(readable),2)
    return(readable, symbol)


