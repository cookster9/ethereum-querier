from etherscan import Etherscan
import time
import datetime
import pandas as pd
import csv

now = int( time.time() )
BREEDING_CONTRACT_ADDRESS = "0x15Cc16BfE6fAC624247490AA29B6D632Be549F00"
API_KEY = "creds.API_KEY"

METAMASK_ADDRESS = "creds.METAMASK_ADDRESS"

eth = Etherscan(API_KEY) # key in quotation marks

# print(eth.get_eth_balance(address=METAMASK_ADDRESS))


# get mint transactions
# start with count
# transactions where method = initiate breeding
FIRST_BREEDING_BLOCK=13424115
CURRENT_BLOCK=eth.get_block_number_by_timestamp(timestamp=now,closest="before")
print("Current block: "+CURRENT_BLOCK)
count=0
transactionList=eth.get_normal_txs_by_address(address=BREEDING_CONTRACT_ADDRESS, startblock=FIRST_BREEDING_BLOCK, endblock=CURRENT_BLOCK, sort="")
#print(eth.get_normal_txs_by_address(address=BREEDING_CONTRACT_ADDRESS, startblock=13773630, endblock=13774615, sort=""))


breedingByDate = []

eventCount = {
}

TOTAL_BABIES=3550
current_count=0
tx_count=0
last_date=''
last_tx={}
for tx in transactionList:
    #print(tx["input"][0:10])
    tx_count=tx_count+1
    if(tx["input"][0:10] == "0x71bf55d4" and tx['isError'] == '0'):
        #print(tx)
        current_count=current_count+1
        epoch=tx["timeStamp"]
        ts=datetime.datetime.fromtimestamp(int(epoch))
        date=ts.strftime('%Y-%m-%d') #date is local CST
        if(date not in eventCount):
            eventCount[date]=0
        eventCount[date]=eventCount[date]+1
        last_date=date
    last_tx=tx

print(last_tx)
last_epoch=last_tx['timeStamp']
ts=datetime.datetime.fromtimestamp(int(last_epoch))
date=ts.strftime('%Y-%m-%d %H-%M-%S %z')
print(date)

print("Total transactions: ",tx_count)

remaining=TOTAL_BABIES-current_count


print("Final size: ",TOTAL_BABIES)
print("Babies bred: ",current_count)
print("Remaining: ",remaining)

eventCount_wrapper = {}

i = 0
for key in eventCount:
    
    eventCount_wrapper[i]=[key, eventCount[key]]
    i=i+1

description_data=pd.DataFrame.from_dict(data=eventCount_wrapper, orient='index', dtype=None, columns=['Date','Count'])

description_data['Rolling7Day'] = description_data['Count'].rolling(7).mean()

description_data['DaysLeftRoll'] = remaining/description_data['Rolling7Day']
description_data['DaysLeftDay'] = remaining/description_data['Count']


print(description_data)

filename='Breeding Event Count'+datetime.datetime.now().strftime("%m%d%Y%H%M%S")+'.csv'
description_data.to_csv(filename, index = False, sep='|')

