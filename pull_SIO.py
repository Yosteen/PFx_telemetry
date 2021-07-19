import requests,urllib3,json,pymongo,time
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#mongodb connection
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["qa"]
creds = db["creds"]
test_coll = db['testp']

#Dynamic Test Variables
row_test = test_coll.find_one({'_id':'00c'})
test_name = row_test['testname']
test_period = int(row_test['test_period'])
pull_frequency = int(row_test['pull_frequency'])

num_of_pulls = int((test_period*60)/pull_frequency)

row_creds = creds.find_one({'_id':'00a'})
username = row_creds['username']
password = row_creds['password']
user = ''
token = row_creds['token']
gw = 'https://192.168.85.100'
login_url = gw + '/api/login'
config_url = gw + '/api/Configuration'
instances_url = gw + '/api/types/System/instances'
qcluster = gw + '/api/instances/System/queryMdmCluster'
qall_url = gw + '/api/types/StoragePool/instances'
url_config = gw + config_url
qsds_url = gw + '/api/types/Sds/instances/action/querySelectedStatistics'
qsdsnetworkltncy = gw + '/api/instances/Sds::20840d2c00000000/action/querySdsNetworkLatencyMeters'
qsys_url = gw + '/api/instances/System::25e4f2ee7c712d0f/relationships/Statistics'

#Create a new Token if the old one is invalid
test = requests.get(config_url, auth=(user,token),verify=False)
if test.status_code != 200:
    print('exectuting if statement')
    tkn = requests.get(login_url, auth=(username,password),verify=False)
    tkn1 = tkn.__dict__
    tkn2 = str(tkn1['_content'])
    tkn3 = (tkn2[3:])
    tkn4 = (tkn3[:-2])
    query = {"_id":"00a"}
    newvalues = {"$set": {"token":tkn4}}
    db.creds.find_one_and_update(query,newvalues)
    token =tkn4

#print info
print('The script will last for ',test_period,'minutes and will pull the system every ',pull_frequency,'seconds for ',num_of_pulls,' times')

for x in range(num_of_pulls):
    #Query the system statistics and calculate total IOPs 
    iop_properties= ["bckRebuildWriteBwc","primaryReadFromDevBwc","totalReadBwc","totalWriteBwc","primaryWriteBwc","secondaryWriteBwc","normRebuildReadBwc","rebalanceWriteBwc","primaryReadBwc","fwdRebuildReadBwc","bckRebuildReadBwc","normRebuildWriteBwc","rebalanceReadBwc","secondaryReadFromDevBwc","secondaryReadBwc","fwdRebuildWriteBwc"]
    iops_arr=[]
    query_sys = (requests.get(qsys_url,auth=(user,token),verify=False)).json()
    for i in iop_properties:
        value = query_sys[f'{i}']
        iops_arr.append(int(value['numOccured']))
    iops = int(sum(iops_arr)/20)

    #Query sds for bandwidth and add it up as a workload
    query_sds_r = requests.post(qsds_url, auth=(user,token),json={'allIds':'',"properties":["totalReadBwc","totalWriteBwc"]},verify=False)
    query_sds = query_sds_r.json()
    kbsarr=[]
    for i in query_sds:
        sds = query_sds[i]
        sds_twr = sds['totalWriteBwc']
        sds_tw = int(sds_twr['totalWeightInKb'])
        kbsarr.append(sds_tw)
        sds_trr = sds["totalReadBwc"]
        sds_tr = int(sds_trr['totalWeightInKb'])
        kbsarr.append(sds_tr)
    workload_r = sum(kbsarr)/10000
    workload = int(workload_r)
    
    #Query system and get Rebuild and Rebalance values
    vvalues = ["activeMovingCapacityInKb","rebalanceCapacityInKb",]
    rbrb=[]         #rebuild reblance array
    for i in vvalues:
        a = str(round((query_sys[i]/1000000),2))
        #print("{0:45} {1} {2:15}".format(i,a,"GB"))
        rbrb.append(a)
    rebuild = rbrb[0]
    rebalance = rbrb[1]
    db.data.insert_one({'bandwidth':workload,'iops':iops,'rebuild':rebuild,'rebalance':rebalance,'testname':test_name,'time':datetime.now()})
    left = num_of_pulls - x
    print (left,' times left |', 'Bandwidth = ',workload,' IOPs = ',iops,' rebuild = ',rebuild,' rebalance = ',rebalance)
    time.sleep(pull_frequency)
