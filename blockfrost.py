# author:       andrjb
# date:         2022-02-10
# description:  includes functions to pull total stake from blockfrost api aswell as                    cneta price from sundaeswap
#---------------------------------------------------------------------------------
import requests
import json
import os
#---------------------------------------------------------------------------------
endpoint = "https://stats.sundaeswap.finance/graphql"
header = '{"query":"query searchPools($query: String) {  pools(query: $query) {    ...PoolFragment  }}fragment PoolFragment on Pool {  apr  assetA {    ...AssetFragment  }  assetB {    ...AssetFragment  }  assetLP {    ...AssetFragment  }  fee  quantityA  quantityB}fragment AssetFragment on Asset {  assetId  policyId  assetName  decimals  ticker  dateListed}","variables":{"query":"cneta"},"operationName":"searchPools"}'
#---------------------------------------------------------------------------------

#Detects and cuts out the amount of tokens in liquidity pool (from API call)
def cut_amount(string, look_for, offset, stop):
  index = string.find(look_for)
  val = ""
  for i in range(index + offset, len(string)):
    val += string[i]
    if string[i+2] == stop: 
      break 
  if offset == 14:
    string = int(round(int(val)/1000000, 0))
  else:
    string = int(val)
  return(string)
#---------------------------------------------------------------------------------

#Pulls total stake of both LISO pools from blockfrost API
def pool():
  response = requests.get(
    url="https://cardano-mainnet.blockfrost.io/api/v0/pools/pool17h6slydr6rd9vquqa38p5cf9xqnpc24w6a99rhllcjzljgugx6x",
    headers=dict(project_id=os.getenv('blockfrostkey'))
  )
  stat1 = response.status_code
  if stat1 == 200:
    json_data = json.loads(response.text)
    result = json.dumps(json_data)
    result = str(result)
    result = cut_amount(result, "live_stake", 14, ",")

  response = requests.get(
    
    url="https://cardano-mainnet.blockfrost.io/api/v0/pools/pool15hx9hze8ulcsw6e7ceelz2pem2g3u9c29wqe4eszkhspj3wcdlx",
    headers=dict(project_id=os.getenv('blockfrostkey'))
  )
  stat2 = response.status_code
  if stat2 == 200:
    json_data = json.loads(response.text)
    result2 = json.dumps(json_data)
    result2 = str(result2)
    result2 = cut_amount(result2, "live_stake", 14, ",")
  
  stat = stat1 + stat2  
  if stat == 400:
    result = result + result2
    result = "{:,}".format(result)
    return(result,stat)
  else: 
    return(0,stat)
  #---------------------------------------------------------------------------------

#Pulls cNeta price from SundaeSwap
def cneta():
  response = requests.post(endpoint, header)

  if response.status_code == 200:
    json_data = json.loads(response.text)
    raw = json.dumps(json_data)
    raw = str(raw)
    result = cut_amount(raw, "quantityA", 13,",")
    result2 = cut_amount(raw, "quantityB", 13,"}")
    price = round((result / 1000000) / result2, 6)
    return(price, response.status_code)
  else:
    return(0, response.status_code)
  #---------------------------------------------------------------------------------
