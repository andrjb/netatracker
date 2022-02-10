# author:       andrjb
# date:         2022-02-10
# description:  functions to pull neta/erg price from ergodex api and erg price from                    coingecko api
#---------------------------------------------------------------------------------
import requests
import json
#---------------------------------------------------------------------------------

#Detects and cuts out the amount of tokens in liquidity pool (from API call)
def cut_amount(string,look_for,stop_at,offset):
  index = string.find(look_for)
  val = ""
  for i in range(index + offset, len(string)):
    val += string[i]
    if string[i+1] == stop_at: 
      break 
  string = float(val) 
  return(string)
#---------------------------------------------------------------------------------

#Makes API call and calculates price with amount of tokens in LP
def get_price():
    response = requests.get(
        "https://api.ergodex.io/v1/amm/pool/7d2e28431063cbb1e9e14468facc47b984d962532c19b0b14f74d0ce9ed459be/stats?from"
    )
    if int(response.status_code) == 200:
      json_data = json.loads(response.text)
      result = json.dumps(json_data)
      ERGamount = str(result[150:200])     #170:185 contains amount (unstable)
      ERGamount = cut_amount(ERGamount, "amount", ',', 9)
      NETAamount = str(result[295:345])     #170:185 contains amount (unstable)
      NETAamount = cut_amount(NETAamount, "amount", ',', 9)
      netergprice = round(((NETAamount / ERGamount) * 1000), 8)
      ergnetprice = round(((ERGamount / NETAamount) / 1000), 8)
      return (netergprice, ergnetprice, int(response.status_code))
    else: 
      print("Error occured: " + str(response.status_code))
      return(0, 0, int(response.status_code))
#---------------------------------------------------------------------------------

#Makes API call and calculates price with amount of tokens in LP
def erg_price():
    response = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?ids=ergo&vs_currencies=usd"
    )
    print(response.status_code)
    if int(response.status_code) == 200:
      json_data = json.loads(response.text)
      result = json.dumps(json_data)
      erg = str(result)
      erg = cut_amount(erg, "usd", '}',6)
      return (erg, int(response.status_code))
    else: 
      print("Error occured: " + str(response.status_code))
      return(0, 0, int(response.status_code))
#---------------------------------------------------------------------------------
