from web3 import Web3
import config
import time
from Cake_Utils import get_status_transaction


"""
    panRouterContractAddress="0x10ED43C718714eb63d5aA57B78B54704E256024E",# PANCAKE CONTRACT
    sender_address = "", # METAMASK ADDRESS
    spend = '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c',# WBNB CONTRACT
    contract_id = "", # TOKEN TO SELL CONTRACT //ccar = 0x50332bdca94673f33401776365b66cc4e81ac81d
    tokenValue = 10, # AMOUNT TOKENS TO SELL
    private_key=config.private, # PRIVATE KEY OF METAMASK
"""

def banana_sell(panRouterContractAddress, sender_address, spend, contract_id, tokenValue, private_key=config.private):
    ## DEFINICAO VARIAVEIS
    bsc = "https://bsc-dataseed.binance.org/"
    web3 = Web3(Web3.HTTPProvider(bsc))

    # ABI CONTRACTS
    panabi = open('Pancake_ABI_Contract.abi', 'r').read()
    sellAbi = open('Pancake_ABI_Sell_Contract.abi', 'r').read()

    # CONTRACT CONFIGURATION
    spend = web3.toChecksumAddress(spend)
    gas_price = web3.toWei('8','gwei')
    contract_id = web3.toChecksumAddress(contract_id)
    contract = web3.eth.contract(address=panRouterContractAddress, abi=panabi)
    sellTokenContract = web3.eth.contract(contract_id, abi=sellAbi)


    # TOKEN CONFIGURATION
    balance = sellTokenContract.functions.balanceOf(sender_address).call()
    tokenValue = web3.toWei(tokenValue, 'ether')

    ##

    ###
    #END
    ###

    ## VERIFICACAO LOGICA

    if web3.isConnected() == False: # Caso não consiga se conectar a WEB3 BSC
        return("web3 problem")
    
    ##

    humanReadable_BNB_BALANCE = web3.fromWei(web3.eth.get_balance(sender_address),'ether')
    if humanReadable_BNB_BALANCE == 0:
        return("insufficiente balance")

    ##

    ###
    #END
    ###


    ## TRANSACTION FIRST PAIR CONFIG
    approve = sellTokenContract.functions.approve(panRouterContractAddress, balance).buildTransaction({'from': sender_address,'gasPrice': gas_price,'gas': 250000,'nonce': web3.eth.get_transaction_count(sender_address)})
    signed_txn = web3.eth.account.sign_transaction(approve, private_key=private_key)
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    while True:
        try: #AGUARDA A TRANSACAO NA BLOCKCHAIN
            FIRST_PAIR = get_status_transaction(tx_token)
            break
        except:
            pass
    
    ###
    #END
    ###
    #

    ## TRANSACTION SECOND PAIR CONFIG
    pancakeswap2_txn = contract.functions.swapExactTokensForETH(tokenValue ,0, [contract_id, spend],sender_address,(int(time.time()) + 1000000)).buildTransaction({'from': sender_address,'gasPrice': gas_price,'gas': 350000,'nonce': web3.eth.get_transaction_count(sender_address)})
    signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=private_key)
    try:
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    except: # caso tenha um erro no gás ou a transacao falhe
        return("gas error")

    while True:
        try: #AGUARDA A TRANSACAO NA BLOCKCHAIN
            SECOND_PAIR = get_status_transaction(tx_token)
            break
        except:
            pass    
    return(FIRST_PAIR, SECOND_PAIR)
