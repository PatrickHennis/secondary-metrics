import json
import requests
from datetime import date

#
def strip_data(json_data):
  bht = json_data['height']
  txs = json_data['tx']

  file = open("data.csv", "a")

  for tx in txs:
    url = 'https://explorer.zensystem.io/insight-api-zen/tx/' + tx
    r = requests.get(url)
    data = r.json()
    num_inputs = len(data['vin'])
    file.write(tx + "," + str(bht) + "," + str(num_inputs) + "\n")
    print("writing")

  file.close()

# get date and get most recent block
date = str(date.today())
url = 'https://explorer.zensystem.io/insight-api-zen/blocks?limit=1&blockDate=' + date

r = requests.get(url)
data = r.json()
# parse json and pull the block hash and time out
bh = data['blocks'][0]['hash']
st = data['blocks'][0]['time']

# calculate total seconds in a month
month_secs = (30 * 24 * 60 * 60)
under_month = True

while under_month:
  # get block info of most recent block
  url = 'https://explorer.zensystem.io/insight-api-zen/block/' + bh
  r = requests.get(url)
  data = r.json()
  # get previous block hash
  bh = data['previousblockhash']
  bt = data['time']
  if ((st - bt) > month_secs):
    under_month = False
  strip_data(data)
