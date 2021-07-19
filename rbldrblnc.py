import requests,urllib3,json,pymongo,time
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Test Variables
test_name = 'badmtu'
test_period = 5        #in minutes
pull_frequency= 5      #in seconds

num_of_pulls = int((test_period*60)/pull_frequency)
#mongodb connection
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["qa"]
creds = db["creds"]
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
query_sys = (requests.get(qsys_url,auth=(user,token),verify=False)).json()
#print  (json.dumps(query_sys,indent=3))
#vvalues = ["bckRebuildCapacityInKb","activeMovingCapacityInKb","degradedHealthyCapacityInKb","fglUserDataCapacityInKb","activeBckRebuildCapacityInKb","rebalanceCapacityInKb","degradedFailedCapacityInKb","activeNormRebuildCapacityInKb","snapCapacityInUseInKb","pendingMovingCapacityInKb","pendingFwdRebuildCapacityInKb", "tempCapacityInKb","normRebuildCapacityInKb","activeRebalanceCapacityInKb","unreachableUnusedCapacityInKb","trimmedUserDataCapacityInKb","netFglUserDataCapacityInKb","netSnapshotCapacityInKb","failedCapacityInKb","pendingRebalanceCapacityInKb","semiProtectedCapacityInKb","bckRebuildCapacityInKb","netTrimmedUserDataCapacityInKb","pendingBckRebuildCapacityInKb","tempCapacityVacInKb","inMaintenanceCapacityInKb","fwdRebuildCapacityInKb","pendingNormRebuildCapacityInKb","movingCapacityInKb","snapCapacityInUseOccupiedInKb","activeFwdRebuildCapacityInKb"]

vvalues = ["activeMovingCapacityInKb","rebalanceCapacityInKb",]
for i in vvalues:
    if query_sys[i] != 0 :
        a = str(round((query_sys[i]/1000000),2))
        print("{0:45} {1} {2:15}".format(i,a,"GB"))
