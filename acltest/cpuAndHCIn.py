##Uses DME Model, had a huge issue with the polling intervals

import requests,json,urllib3,os,xmltodict
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#os.system('clear')
user='admin'
password=''

headers = {'cache-control': "no-cache"}
switches =['10.234.112.60']


for ip in switches:
    swUrl = 'http://' + ip
    loginUrl = swUrl + '/api/aaaLogin.json'
    pld1 = '{aaaUser:{attributes:{name:'
    pld2 = 'a'
    pld3= '}}}'
    payload = f'{pld1}{user},pwd:{password}{pld3}'
    response = requests.request("POST", loginUrl, data=payload, headers=headers)
    #print (response.status_code)
    response = response.json()
    imdata = response['imdata']
    tokenbody = imdata[0]
    aaaLogin = tokenbody['aaaLogin']
    attributes = aaaLogin['attributes']
    token = attributes['token']
    cookiesDic = {'APIC-Cookie':token}
    cpuHisUrl = swUrl + '/api/node/mo/sys/procsys/syscpusummary/syscpuhistory-last60seconds.xml?query-target=self'
    cpuHisrqst = requests.get(cpuHisUrl,cookies=cookiesDic, verify=False)
    cpuHis = xmltodict.parse(cpuHisrqst.text)
    sxtyMinsAvg = cpuHis['imdata']["procSysCpuHistory"]["@usageAvg"]
    sxtyMins = round(float(sxtyMinsAvg),2)
    print ("Switch ",ip,"60 seconds Average => ",sxtyMins)
    interfaceUrl = swUrl + '/api/node/mo/sys/intf/phys-%5Beth1/3%5D.xml?query-target=children'
    interfacerqst = requests.get(interfaceUrl,cookies=cookiesDic,verify=False)
    interfaceData = xmltodict.parse(interfacerqst.text)
    rmonIFHCIn = (interfaceData['imdata']["rmonIfHCIn"])
    print (json.dumps(rmonIFHCIn,indent=4))




    #print(json.dumps(cpusIdle,indent=4))


