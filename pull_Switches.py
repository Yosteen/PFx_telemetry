import requests,json,urllib3,sys,pymongo,time
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#mongodb connection
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["qa"]
test_coll = db['testp']

#Test Variables
row_test = test_coll.find_one({'_id':'00c'})
test_name = row_test['testname']
test_period = int(row_test['test_period'])
pull_frequency = int(row_test['pull_frequency'])

num_of_pulls = int((test_period*60)/pull_frequency)

user='admin'
password='Rtp@1234'

sws =['10.234.112.32','10.234.112.33','10.234.112.34','10.234.112.35']

headers = {'Content-Type': 'application/json'}
interfaces = ['e1/22','e1/24']
dbdict = {}
for x in range(num_of_pulls):
  dbdict = {}
  for sw in sws:
    url ='https://'+ sw + '/ins'
    octet = sw[-2:]
    for interface in interfaces:
      payload={"ins_api":{"version": "1.0","type": "cli_show","chunk": "0","sid": "1","input": f'show interface {interface}',"output_format": "json"}}
      r = requests.post(url,data=json.dumps(payload),headers=headers,auth=(user,password),verify=False).json()
      in_rate = int(int(r['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface']['eth_inrate1_bits'])/1000000)
      out_rate = int(int(r['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface']['eth_outrate1_bits'])/1000000)
      dbinput_sw = {octet+'-'+interface:(in_rate+out_rate)}
      dbdict.update(dbinput_sw)
  dbdict.update({'testname':test_name})
  dbdict.update({'time':datetime.now()})
  db.switch.insert_one(dbdict)
  left = num_of_pulls - x
  print (left,' times left')
  time.sleep(pull_frequency)