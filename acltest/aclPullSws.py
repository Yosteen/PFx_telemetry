import requests,json,urllib3,sys,pymongo,time,os
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.system('clear')
#mongodb connection
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["acldb"]
criteriaCollction = db['tcriteria']
switchesCollecion = db['switches']

#Test Variables
row_test = criteriaCollction.find_one({'_id':'00c'})
testName = row_test['testname']
test_period = int(row_test['test_period'])
interval = int(row_test['pull_frequency'])

numOfPolls = int((test_period*60)/interval)

#num_of_pulls=1
user='admin'
password=''

sws =['10.234.112.60','10.234.112.61']

headers = {'Content-Type': 'application/json'}
interfaces = ['e1/3','e1/4']
dbDict = {}
timeStamp = 0
for x in range(numOfPolls):
  timeStamp = timeStamp + interval
  dbDict = {}
  totalRate=[]
  for sw in sws:
    url ='https://'+ sw + '/ins'
    octet = sw[-2:]
    swId = 'sw'+octet
    cpuCMD = {"ins_api":{"version": "1.0","type": "cli_show","chunk": "0","sid": "1","input": 'show process cpu history data',"output_format": "json"}}
    cpuRqst = requests.post(url,data=json.dumps(cpuCMD),headers=headers,auth=(user,password),verify=False).json()
    cpu_avg_60sec = cpuRqst['ins_api']['outputs']['output']['body']["TABLE_processes_cpu_history"]["ROW_processes_cpu_history"]
    cpu10secArr = []
    for sec in range (10):
      cpu10secArr.append(cpu_avg_60sec[sec]['cpu_avg_sec'])
    cpu10secAvg = sum(cpu10secArr)/len(cpu10secArr)
    #print(sw," CPU 10 Seconds Average => ",cpu10secAvg)
    dbDict.update({swId:cpu10secAvg})
    
    
    for interface in interfaces:
      interfaceCMD={"ins_api":{"version": "1.0","type": "cli_show","chunk": "0","sid": "1","input": f'show interface {interface}',"output_format": "json"}}
      interfceRqst = requests.post(url,data=json.dumps(interfaceCMD),headers=headers,auth=(user,password),verify=False).json()
      in_rate = int(int(interfceRqst['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface']['eth_inrate1_bits'])/1000000)
      out_rate = int(int(interfceRqst['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface']['eth_outrate1_bits'])/1000000)
      totalRate.append(in_rate)
      totalRate.append(out_rate)
      #print (json.dumps(cpu_avg_60sec,indent=4))
      #print("Bandwidth  => ",in_rate+out_rate)
  #print (totalRate)
  swBandwidth = sum(totalRate)
  dbDict.update({'swbandwidth':swBandwidth})   
  dbDict.update({'testName':testName}) 
  dbDict.update({'timeStamp':timeStamp})
  print (dbDict)  
  switchesCollecion.insert_one(dbDict)
  left = numOfPolls - x
  print (left,' times left')
  time.sleep(interval)  
  
  
