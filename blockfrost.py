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
def cut_amount(string, look_for, offset, stop, stopind):
  index = string.find(look_for)
  val = ""
  for i in range(index + offset, len(string)):
    val += string[i]
    if string[i+stopind] == stop: 
      break 
  if offset == 14:
    string = int(round(int(val)/1000000, 0))
  else:
    string = int(val)
  return(string)
#---------------------------------------------------------------------------------

#Creates output string for stake pool infos
def formatstake(st1,st2,del1,del2,bl1,bl2):
  stake = st1 + st2
  stake = "{:,}".format(stake)
  deleg = del1 + del2
  st1 = "{:,}".format(st1)
  st2 = "{:,}".format(st2)
  s = "**NETA1:**\nLive Stake: " + str(st1) + " ADA"+ "\nDelegators: " + str(del1) + "\nBlocks this epoch: " + str(bl1) + "\n-----------------------------------\n" + "**NETA2:**\nLive Stake: " + str(st2) + " ADA" + "\nDelegators: " + str(del2) + "\nBlocks this epoch: " + str(bl2) + "\n-----------------------------------\n" + "**Total:** \n" + "Live Stake: " + str(stake) + " ADA" + "\nDelegators: " + str(deleg)
  return(s)
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
    raw = json.dumps(json_data)
    raw = str(raw)
    stake = cut_amount(raw, "live_stake", 14, ",", 2)
    delegators1 = cut_amount(raw, "live_delegators", 18, ",", 1)
    block1 = cut_amount(raw, "blocks_epoch", 15, ",", 1)

  response = requests.get(
    
    url="https://cardano-mainnet.blockfrost.io/api/v0/pools/pool15hx9hze8ulcsw6e7ceelz2pem2g3u9c29wqe4eszkhspj3wcdlx",
    headers=dict(project_id=os.getenv('blockfrostkey'))
  )
  stat2 = response.status_code
  if stat2 == 200:
    json_data = json.loads(response.text)
    raw2 = json.dumps(json_data)
    raw2 = str(raw2)
    stake2 = cut_amount(raw2, "live_stake", 14, ",", 2)
    delegators2 = cut_amount(raw2, "live_delegators", 18, ",", 1)
    block2 = cut_amount(raw2, "blocks_epoch", 15, ",", 1)
  
  stat = stat1 + stat2  
  if stat == 400:
    s = formatstake(stake, stake2, delegators1, delegators2, block1, block2)
    return(s, stat)
  else: 
    return(0, stat)
  #---------------------------------------------------------------------------------

#Pulls cNeta price from SundaeSwap
def cneta():
  response = requests.post(endpoint, header)
  if response.status_code == 200:
    json_data = json.loads(response.text)
    raw = json.dumps(json_data)
    raw = str(raw)
    result = cut_amount(raw, "quantityA", 13,",", 2)
    result2 = cut_amount(raw, "quantityB", 13,"}", 2)
    price = round((result / 1000000) / result2, 6)
    return(price, response.status_code)
  else:
    return(0, response.status_code)
  #---------------------------------------------------------------------------------
