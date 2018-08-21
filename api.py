import requests
import json


class API:

    def __init__(self,db):
        self.database=db
        self.base_url="https://min-api.cryptocompare.com/data/pricemultifull?fsyms=XRP,EBTC&tsyms=USD,EUR"
        print("there are "+str(db.get_number_of_coins()))
        if db.get_number_of_coins()==0 :
            print("Requesting data.... ")
            self.get_coin_names()


        self.refresh_coins(db)


    def get_coin_names(self):
        url="https://www.cryptocompare.com/api/data/coinlist/"
        data = requests.get(url).json()
        data=data["Data"]
        coin_symbols=data.keys()
        for symbol in coin_symbols:
            coin_data=data[symbol]
            print("inserting "+ coin_data["CoinName"] +" symbol "+ symbol)
            self.database.insert_coin_name(coin_data["CoinName"],symbol)



    def refresh_coins(self,db):

        if db.get_number_of_investments()==0:
            return ;
        coins=db.get_investments_symbols()
        coins=map(lambda x:x.upper(),coins)
        coin_string=",".join(coins )
        self.base_url="https://min-api.cryptocompare.com/data/pricemultifull?fsyms="+coin_string+"&tsyms=USD,EUR"
        print(self.base_url)
        data = requests.get(self.base_url).json()
        data=data["RAW"]
        coins=data.keys()
        print (coins)
        for coin in coins:
            print ("coin is "+coin)
            coin_data=data[coin]
            coin_currency=coin_data.keys()
            for currency in coin_currency:
                currency=coin_data[currency]

                print("inserting "+ str(currency["FROMSYMBOL"]) +" price "+ str(currency["PRICE"]))
                self.database.insert_coin("name", currency["FROMSYMBOL"],  currency["PRICE"], currency["VOLUMEDAY"],
                                          currency["MKTCAP"],currency["SUPPLY"],currency["OPEN24HOUR"],
                                          currency["HIGH24HOUR"],currency["LOW24HOUR"],currency["TOSYMBOL"],currency["LASTUPDATE"])
