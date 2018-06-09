import json
import requests
from datetime import date

# strip data from json and write to file
def strip_data(json_data, bs):
    bht = json_data['height']
    txs = json_data['tx']

    file = open("data.csv", "a")

    for tx in txs:
        url = 'https://explorer.zensystem.io/insight-api-zen/tx/' + tx
        r = requests.get(url)
        data = r.json()
        num_inputs = len(data['vin'])
        file.write(tx + "," + str(bht) + "," + str(num_inputs) + "," + str(bs) + "\n")

    file.close()

def main_run(url, st):
    month_secs = (30 * 24 * 60 * 60)
    under_month = True
    try:
        while under_month:
            # get block info of most recent block
            r = requests.get(url)
            data = r.json()
            # get previous block hash
            bh = data['previousblockhash']
            bt = data['time']
            bs = data['size']
            if ((st - bt) > month_secs):
                under_month = False
            strip_data(data, bs)
            url = 'https://explorer.zensystem.io/insight-api-zen/block/' + bh
    except:
        recover()

def recover():
    fileHandle = open ( 'data.csv',"r" )
    lineList = fileHandle.readlines()
    fileHandle.close()
    lline = lineList[len(lineList)-1]
    fline = lineList[0]
    tx = lline[:64]
    url = 'https://explorer.zensystem.io/insight-api-zen/tx/' + tx
    r = requests.get(url)
    data = r.json()
    bh = data['blockhash']
    tx = fline[:64]
    url = 'https://explorer.zensystem.io/insight-api-zen/tx/' + tx
    r = requests.get(url)
    data = r.json()
    st = data['time']
    url = 'https://explorer.zensystem.io/insight-api-zen/block/' + bh
    main_run(url, st)

def main():
    # get date and get most recent block
    d = str(date.today())
    url = 'https://explorer.zensystem.io/insight-api-zen/blocks?limit=1&blockDate=' + d
    r = requests.get(url)
    data = r.json()
    # parse json and pull the block hash and time out
    bh = data['blocks'][0]['hash']
    st = data['blocks'][0]['time']

    # calculate total seconds in a month
    url = 'https://explorer.zensystem.io/insight-api-zen/block/' + bh
    try:
        # if was previously running and failed, remove the bh from the url, it will go straight to recovery method
        main_run(url, st)
    except:
        recover()


if __name__ == "__main__":main()
