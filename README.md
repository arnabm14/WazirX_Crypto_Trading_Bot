# WazirX Crypto Trading Bot

This is my personal project which uses the live market data from the Wazirx API to perform various operations as listed below along with the WazirX API Documentation on how to use it .

Freelance Tech Article writer.
Article Links  : https://www.analyticsvidhya.com/blog/author/arnab1408/

`wazirtext.py` - This file can read the live market data and send a whatsapp notification to the desired group regarding the price fluctuations in the last 5 minutes. You need to manually scan the web.whatsapp.com QR code in the beginning and need to make sure that whsatsapp account is added to the groups you need to send he text to. The default Alert paramaters are 5% and 25% respectively and I have setup two groups for crucial and important alerts. It can be commented out or filtered accordingly. The chromedriver is by default set to be in the same location as the python file which can be changed in side the code. The data is written to Stock.csv every minute to keep track of historical data since WazirX does not allow that yet. Data Analysis can be done on it to understand the market trends.

`wazirX_Price_Volume.py` - This file develops on the previous python file "wazirtext.py" and adds functionality like threading, Price and Volume monitoring and better error handling. Default Alert parameters for Price and Volume are mentioned in the code and can be changed according to one's convenience. All the above parameters are required for this code too. CHromedriver and whatsapp account. The data is written to Stockvol.csv and vol.csv regarding the stock price and volume of the stock traded in the last 24hrs.

`RNN_Wazirx_Trading_Bot.py` - This file uses a RNN algorithm to train a model where you can set your custom "Window_Size" and "Episodes" or the number of Epoch for the model to train for. Generally if the window size is of the format 10^n, then the episode size should ne 'n-1'. I will keep updating this paragraph as the model and results develop. The CSV data has 13k rows of data and after the first 7000, the data till the end is continuous. 

`LSTM_WazirX_Train.py` - This file uses a LSTM model which is faster than RNN and computes the data and there is another file `LSTM_WazirX_Test.py` which can be used just to test the model. THe train module is by default coded to look back 200 minutes and predict the next output which can be changed along with the number of units in the LSTM. The last 90 minutes of data are added artificially and the end goal is to predict that accurately.


# WazirX Public Rest API
Here’s our public API handed to you on a silver platter. You can use it to build tickers, price comparison apps, or anything that helps the crypto community. Use it responsibly. ❤️


## General Information
1. Base API Endpoint: https://api.wazirx.com
1. All public api will return either JSON or Array object.

### Public API Endpoints

1. #### MARKET STATUS
   GET `/api/v2/market-status`  [Live link](https://api.wazirx.com/api/v2/market-status)

    > "Market Status" will give your an overview of markets and assets. This is helpful when you want to track the configuration of our markets, track fees or status of withdrawal deposit, market configuration and more. This response is not recommended for price polling because accurate realtime price is not guaranteed as there could be some delays. We recommend using price ticker API for all price tracking activity.
    
    Response object will have 2 keys `markets`(all market related configs will be in this key) and `assets`(all assets related configs will be here). 
    ### Response:
    ```
    {
        "markets": [
            {
                "baseMarket": "btc",
                "quoteMarket": "inr",
                "minBuyAmount": 0.001,
                "minSellAmount": 0.001,
                "fee": {
                    "bid": {
                        "maker": 0.001,
                        "taker": 0.0025
                    },
                    "ask": {
                        "maker": 0.001,
                        "taker": 0.0025
                    }
                },
                "basePrecision": 4,
                "quotePrecision": 2,
                "low": "460001.01",
                "high": "505000.0",
                "last": "480102.0",
                "open": 505002,
                "volume": "0.2071",
                "sell": "490000.0",
                "buy": "485001.0",
                "type": "SPOT"
                "Status": "active"
            },
            ...
        ],
        "assets": [
            {
                "type": "inr",
                "name": "Rupee",
                "withdrawFee": 0,
                "minWithdrawAmount": 50,
                "maxWithdrawAmount": 50000,
                "minDepositAmount": 500,
                "confirmation": 5,
                "deposit": "enabled",
                "withdrawal": "enabled"
                
            },
            ...
        ]
    }
    ```
    
    
    1. **`markets` key has multiple market related configuration, and description of every field in market is as below:**
    
        1. `baseMarket`: ticker code of base asset
        1. `quoteMarket`: ticker code of quote asset
        1. `minBuyAmount`: Minimum buy amount of base asset
        1. `minSellAmount`: Minumum sell amount of base asset
        1. `fee`: JSON Object consists of `bid` and `ask` order's maker-taker fee percentage
        1. `basePrecision`: Maximum precision of base asset, this the decimal point. 
        1. `quotePrecision`: Maximum  precision of quote asset
        1. `low`: 24 hrs lowest price of base asset
        1. `high`: 24 hrs highest price of base asset
        1. `last`: Last traded price in current market
        1. `open`: Market Open price 24hrs ago
        1. `volume`: Last 24hrs traded volume
        1. `sell`: Top ask order price
        1. `buy`: Top bid order price
        1. `type`: This defines the type of market, currently we have `SPOT` and `P2P`
        1. `status`: This defines the current state of the market. This can be `active` or `suspended`
    1. **`assets` key have multiple asset related configuration as described below:**
    
        1. `type`: asset code
        1. `name`: Display name of asset
        1. `withdrawFee`: Withdrawal fee of asset
        1. `minWithdrawAmount`: Minimum withdrawal amount in a single transaction
        1. `maxWithdrawAmount`: Maximum withdrawal amount in a single transaction
        1. `minDepositAmount`: This is the min Deposit amount that will be accepted as deposit
        1. `confirmations`: Is the min number of block height needed to confirm a block chain deposit transaction.
        1. `deposit`: Denotes whether deposit is enabled or disabled
        1. `withdrawal`: Denotes whether withdrawal is enabled or disabled
        


1. #### MARKET TICKER
   GET `/api/v2/tickers` [Live link](https://api.wazirx.com/api/v2/tickers)
    > Get the latest market heart-beat for all the markets for the last 24hrs.
    
    Returns JSON response which has active market data with all ticker related values.
    ### Response:
    ```
    {
        "btcinr": {
            "base_unit": "btc",
            "quote_unit": "inr",
            "low": "472005.0",
            "high": "508102.0",
            "last": "508100.0",
            "open": 490000,
            "volume": "0.2709",
            "sell": "508100.0",
            "buy": "481000.0",
            "name": "BTC/INR",
            "at": 1536732262
        },
        ...
    }
    ```
    Response has multiple key which denotes market data, this is in JSON. Find all the fields below:
    
    1. `base_unit`: ticker code of base market
    1. `quote_unit`: ticker code of quote asset
    1. `low`: 24 hrs lowest price of base asset
    1. `high`: 24 hrs highest price of base asset
    1. `last`: Last traded price in current market
    1. `open`: Market Open price 24hrs ago
    1. `volume`: Last 24hrs traded volume
    1. `sell`: Top ask order price
    1. `buy`: Top bid order price
    1. `name`: Display text of market
    1. `at`: Timestamp when ticker information is fetched
    

1. #### MARKET DEPTH
   GET `/api/v2/depth` [Live link](https://api.wazirx.com/api/v2/depth?market=btcusdt)
    > Get market orderbook of any market
    
    Returns JSON response which has order book of a perticular market
    ### Response:
    ```
    {
    "timestamp":1559561187,
    "asks":[
               ["8540.0","1.5"],
               ["8541.0","0.0042"]
           ],
    "bids":[
               ["8530.0","0.8814"],
               ["8524.0","1.4"]
           ]
    }
    ```
    1. `["8540.0","1.5"]` : [ PRICE, VOLUME ]
    1. URL param `market=btcusdt` : Replace this with any market to get the desired order book.
    
1. #### MARKET TRADE HISTORY
   GET `/api/v2/trades` [Live link](https://api.wazirx.com/api/v2/trades?market=btcusdt)
    > Get trade history of a market
    
    Returns JSON response which has trade history of a perticular market
    ### Response:
    ```
    [
      {
         "id":1302646,
         "price":"8530.0",
         "volume":"0.3207",
         "funds":"2735.571",
         "market":"btcusdt",
         "created_at":"2019-06-03T17:03:41+05:30",
         "side":null
       }  
   ...
   ]
    ```
    1. URL param `market=btcusdt` : Replace this with any market to get the desired order book.
    
    
If you have any questions regarding APIs, please reach out to us at http://support.wazirx.com
