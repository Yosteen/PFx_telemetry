import time,json,pymongo
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt 


#variables
test_name = 'badvlan'
#mongodb connection
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["qa"]

test_row = db.testp.find_one({'_id':'00c'})
period = test_row['test_period']
interval = test_row['pull_frequency']

query = db.data.find({'testname':test_name})
bw_arr = []
time_arr = []
iops_arr =[]
rebalance_arr = []
rebuild_arr = []
for i in query:
    bw_arr.append(i['bandwidth'])
    time_arr.append(i['time'].strftime("%M:%S"))
    iops_arr.append(i['iops'])
    rebuild_arr.append(i['rebuild'])
    rebalance_arr.append(i['rebalance'])

plt.figure(num=1)
plt.plot(time_arr,bw_arr)
plt.xticks(time_arr,'')
plt.xlabel(f'{interval} seconds interval for {period} mins')
plt.ylabel('Bandwidth in MB')
plt.title('SIO Bandwidth VLAN mismatch')
plt.savefig('/flask/static/time_bw_VLAN_mismatch')

plt.figure(num=2)
plt.plot(time_arr,iops_arr)
plt.xticks(time_arr,'')
plt.xlabel(f'{interval} seconds interval for {period} mins')
plt.ylabel('iops')
plt.title('SIO IOPs VLAN mismatch')
plt.savefig('/flask/static/time_iops_VLAN_mismatch')

plt.figure(num=3)
plt.plot(time_arr,rebuild_arr,time_arr,rebalance_arr)
plt.xticks(time_arr,'')
plt.xlabel(f'{interval} seconds interval for {period} mins')
plt.ylabel('rebuild/rebalance')
plt.title('rebuild/rebalance VLAN mismatch')
plt.savefig('/flask/static/rebuild_rebalance_VLAN_mismatch')


switch_interfaces = ['32-e1/22','32-e1/24','33-e1/22','33-e1/24','34-e1/22','34-e1/24','35-e1/22','35-e1/24']

rows = db.switch.find({"testname":test_name})
arr1 = []
for row in rows:
    arr1.append(row["32-e1/24"])

rows = db.switch.find({"testname":test_name})
arr2 = []
for row in rows:
    arr2.append(row["32-e1/22"])

arr3 = []
rows = db.switch.find({"testname":test_name})
for row in rows:
    arr3.append(row["33-e1/24"])

rows = db.switch.find({"testname":test_name})
arr4 = []
for row in rows:
    arr4.append(row["33-e1/22"])

arr5 = []
rows = db.switch.find({"testname":test_name})
for row in rows:
    arr5.append(row["34-e1/24"])

rows = db.switch.find({"testname":test_name})
arr6 = []
for row in rows:
    arr6.append(row["34-e1/22"])

arr7 = []
rows = db.switch.find({"testname":test_name})
for row in rows:
    arr7.append(row["35-e1/24"])

rows = db.switch.find({"testname":test_name})
arr8 = []
for row in rows:
    arr8.append(row["35-e1/22"])

rows = db.switch.find({"testname":test_name})
arrt = []
for row in rows:
    arrt.append(row["time"].strftime("%M:%S"))

plt.figure(num=4)
plt.plot(arrt,arr1,arrt,arr2,arrt,arr3,arrt,arr4,arrt,arr5,arrt,arr6,arrt,arr7,arrt,arr8)
plt.xticks(arrt,'')
plt.xlabel(f'{interval} seconds interval for {period} mins')
plt.ylabel('Interface BW in MB')
plt.title('Switch interfaces BW VLAN mismatch')
plt.savefig('/flask/static/VLAN_mismatch-switch')
