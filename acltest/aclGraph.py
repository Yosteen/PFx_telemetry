import json,pymongo
import pandas as pd
from matplotlib import pyplot as plt 

#variables
#testName = 'fiveMinNoAcl'
#mongodb connection
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["acldb"]
criteriaCollection = db['tcriteria']

criteriaRow = criteriaCollection.find_one({'_id':'00c'})
period = criteriaRow['test_period']
interval = criteriaRow['pull_frequency']
testName = criteriaRow['testname']

timeArr=[]
sw1CpuArr=[]
sw2CpuArr=[]
bwArr=[]
query = db.switches.find({'testName':testName})
for entry in query: 
    timeArr.append(entry['timeStamp'])
    sw1CpuArr.append(entry['sw60'])
    sw2CpuArr.append(entry['sw61'])
    bwArr.append(entry['swbandwidth'])
#print (timeArr)
#print (sw1CpuArr)
#print (sw2CpuArr)
#print (bwArr)

plt.figure(num=1)
plt.plot(timeArr,bwArr)
plt.xticks(timeArr,'')
plt.xlabel(f'{interval} seconds interval for {period} mins')
plt.ylabel('Bandwidth in Mb')
plt.title('Aggregate SDS Server Bandwidth')
plt.savefig('/flask/acltest/bwaccessmap.png')

plt.figure(num=2)
plt.plot(timeArr,sw1CpuArr)
plt.plot(timeArr,sw2CpuArr)
plt.xticks(timeArr,'')
intInterval,intPeriod = int(interval),int(period)
plt.xlabel(f'{intInterval} seconds interval for {intPeriod} mins')
plt.ylabel('TORs CPU Utilization')
plt.title('Switches CPU Percentage')
plt.savefig('/flask/acltest/cpaccessmap.png')

