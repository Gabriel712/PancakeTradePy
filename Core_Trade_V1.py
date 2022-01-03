from pancakeSell import *
from pancakeBuy import *
from Cake_Utils import *

## VARS EXCHANGE
panRouterContractAddress="0x10ED43C718714eb63d5aA57B78B54704E256024E" # Pancake Contract
sender_address = "" # Your Wallet Address
tokenToBuy="0x50332bdca94673f33401776365b66cc4e81ac81d" #Token to buy ccar=0x50332bdca94673f33401776365b66cc4e81ac81d
spend = '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c'# WBNB Contract
value_BNB_buy = 0.010 # BNB Value to buy

comprar = False # If True, buy token
trade = True # If True, sell token
repeat_x = 1 # Max repeat trades

## VARS TRADE
stop_loss = 500 # USD
stop_gain = 520 # USD
buy_when = 510 # value token / USD


## GET TOKEN AMOUNT IN WALLET
info_token = get_token_amount(sender_address, tokenToBuy)
holded_coin = info_token[0]
symbol = info_token[1]

if trade == True:
    print(f"Trade Configurations\nSTOP LOSS:{stop_loss}\nSTOP GAIN:{stop_gain}\nPRICE TOKEN:{round(get_price(tokenToBuy),2)}")    

for i in range(repeat_x):
    if comprar == True:
        if sniper_token(tokenToBuy, buy_when) == True:
            response_txn = banana_buy(panRouterContractAddress, sender_address, tokenToBuy, spend, value_BNB_buy)
            print(response_txn)
            while True:
                try:
                    x = get_status_transaction(response_txn)["status"]
                    if x == 1:
                        print(f"SUCCESS BUY:\nHash:{response_txn}")
                        new_holded = get_token_amount(sender_address, tokenToBuy)[0]
                        print(f"AMOUNT: {holded_coin - new_holded}")
                        break
                    elif x == 0:
                        print("FAIL :\nMAYBE GAS FEED LOW")
                except:
                    pass

    if trade == True:
        token_price = round(get_price(tokenToBuy),2)
        
        while True:
            info_token = get_token_amount(sender_address, tokenToBuy)
            holded_coin = info_token[0]

            if token_price <= stop_loss:
                print("LOSS")
                print(banana_sell(panRouterContractAddress, sender_address, spend, tokenToBuy, int(holded_coin)))
                break
            elif token_price >= stop_gain:
                print("GAIN")
                print(banana_sell(panRouterContractAddress, sender_address, spend, tokenToBuy, int(holded_coin)))
                break
            token_price = round(get_price(tokenToBuy),2)
            