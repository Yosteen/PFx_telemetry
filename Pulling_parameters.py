import requests,json,urllib3,sys,pymongo,time
from datetime import datetime

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["qa"]

test_name = 'badvlan'
test_period = 30       #in minutes
pull_frequency = 10    #in seconds

query = {'_id':'00c'}
newvalues = {"$set":{'testname':test_name,'test_period':test_period,'pull_frequency':pull_frequency}}
db.testp.find_one_and_update(query,newvalues)
