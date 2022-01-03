from web3 import Web3
import config
import time

"""
    panRouterContractAddress="0x10ED43C718714eb63d5aA57B78B54704E256024E", # PANCAKE CONTRACT
    sender_address = '0x2349967A8edA8FC1EE1bA2236F8cc53b36dca0b4', # METAMASK ADDRESS
    tokenToBuy='0x50332bdca94673f33401776365b66cc4e81ac81d', #TOKEN ADDRESS TO BUY/ ccar=0x50332bdca94673f33401776365b66cc4e81ac81d
    spend = '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c',# WBNB CONTRACT
    amount_minimum_buy = 10000000000 / set to 0, or specify minimum amount of tokeny you want to receive - consider decimals!!!
    value_BNB_buy = 0.010, # BNB VALUE TO USE
    private_key=config.private # PRIVATE KEY METAMASK
"""

def banana_buy(panRouterContractAddress,sender_address,tokenToBuy,spend,value_BNB_buy,private_key=config.private):

    bsc = "https://bsc-dataseed.binance.org/"
    web3 = Web3(Web3.HTTPProvider(bsc))

    if web3.isConnected() == False: # Caso não consiga se conectar a WEB3 BSC
        return(None)

    spend = web3.toChecksumAddress(spend)
    tokenToBuy = web3.toChecksumAddress(tokenToBuy)

    panabi = open('Pancake_ABI_Contract.abi', 'r').read()

    humanReadable_BNB_BALANCE = web3.fromWei(web3.eth.get_balance(sender_address),'ether')
    if humanReadable_BNB_BALANCE == 0:
        return(None)

    contract = web3.eth.contract(address=panRouterContractAddress, abi=panabi)
    nonce = web3.eth.get_transaction_count(sender_address)

    amount_minimum_buy = 10000000000

    start = time.time()


    pancakeswap2_txn = contract.functions.swapExactETHForTokens(
    amount_minimum_buy, #10000000000 set to 0, or specify minimum amount of tokeny you want to receive - consider decimals!!!
    [spend,tokenToBuy],
    sender_address,
    (int(time.time()) + 10000)
    ).buildTransaction({
    'from': sender_address,
    'value': web3.toWei(value_BNB_buy,'ether'),
    'gas': 250000, # maximo gas
    'gasPrice': web3.toWei('8','gwei'),
    'nonce': nonce,
    })

    signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key)
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return(web3.toHex(tx_token))



