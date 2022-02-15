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

#Makes API call from coingecko
def erg_price():
    response = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?ids=ergo&vs_currencies=usd"
    )
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

#Makes API call from coingecko
def ada_price():
    response = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?ids=cardano&vs_currencies=usd"
    )
    if int(response.status_code) == 200:
      json_data = json.loads(response.text)
      result = json.dumps(json_data)
      ada = str(result)
      ada = cut_amount(ada, "usd", '}',6)
      return (ada, int(response.status_code))
    else: 
      print("Error occured: " + str(response.status_code))
      return(0, 0, int(response.status_code))
#---------------------------------------------------------------------------------

#builds table for stickied price post
def buildtable(netergprice, ergnetprice, cnetaprice, erg, ada):
  netusd = ergnetprice*erg
  cnetusd = cnetaprice*ada
  netergstr = f"{netergprice:.5f}"
  cnetaprstr = f"{cnetaprice:.5f}"
  ergstr = f"{erg:.5f}" 
  adastr = f"{ada:.5f}" 
  netusdstr = f"{netusd:.5f}" #
  cnetusdstr = f"{cnetusd:.5f}" 
  s = '```' + '\n┌───────────┬───────────┬──────┐' + '\n│ Pair      │ Price     │ curr │''\n├───────────┼───────────┼──────┤'+ '\n│ NETA/ERG  │ ' + netergstr + ' │' +   ' NETA │' +'\n├───────────┼───────────┼──────┤' + '\n│ NETA/USD  │ ' + netusdstr + '   │' + ' USD  │' +'\n├───────────┼───────────┼──────┤' + '\n│ cNETA/ADA │ '+cnetaprstr+'   │'+     ' ADA  │' +'\n├───────────┼───────────┼──────┤' + '\n│ cNETA/USD │ ' + cnetusdstr + '   │' + ' USD  │' +'\n├───────────┼───────────┼──────┤' + '\n│ ADA/USD   │ ' + adastr + '   │' +    ' USD  │' +'\n├───────────┼───────────┼──────┤' + '\n│ ERG/USD   │ ' + ergstr + '   │' +    ' USD  │' +'\n└───────────┴───────────┴──────┘' + '\n table updates every 30 seconds' + '```'
  return(s)
#---------------------------------------------------------------------------------
