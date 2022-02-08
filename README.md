# netatracker
A simple Discord bot that pulls the current NETA/ERG price from the ErgoDEX API. Can be used as sidebar bot and can send current price in a message on command. 
## How to use 
When sending ```$``` the bot will send a message including the recent NETA/ERG and ERG/NETA valuation. 
The current NETA/ERG valuation is also included in the bots activity. This means this bot can also be used as a sidebar bot. 

Note: ```$``` pulls the most recent data from the [ErgoDEX API](https://api.ergodex.io/v1/amm/pool/7d2e28431063cbb1e9e14468facc47b984d962532c19b0b14f74d0ce9ed459be/stats?from) this data seems to show slightly different valuations than the DEX from time to time but should be more or less accurate. The activity section of the bot pulls data from this API at one minute intervals. 

Feel free to fork and modify this code as you wish. 
