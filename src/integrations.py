import os
import requests
import sys

class TriggerFireSimulations:
    def __init__(self,authURL,proxyUrl):
        authToken = self.getAuthToken(authURL)
        if 'token' in authToken:
            self.headers = {'content-type': "application/json",
                            'authorization': 'Bearer ' + authToken['token']}
        else:
            sys.exit('Error with auth token: ' + str(authToken))
        self.farsiteParams = self.getDefaultParams()
        self.proxyUrl = proxyUrl
        
    def getAuthToken(self,authURL):
        userName = os.getenv('AUTHUSERNAME')
        password = os.getenv('AUTHPASSWORD')

        if userName is None:
            raise EnvironmentError("Failed because {} is not set.".format('AUTHUSERNAME'))
        if password is None:
            raise EnvironmentError("Failed because {} is not set.".format('AUTHPASSWORD'))
        
        authURL1 = authURL+'?user='+ userName + '&password=' + password

        r = requests.request('GET',authURL1)
        authToken = r.json()
        if r.status_code==200 and 'token' in authToken:
            return authToken
        else:
            sys.exit('Error with auth endpoint')

    def getDefaultParams(self):
        defaultParams = {"hours": 3,
                        "ember": 80,
                        "ignition": {
                            "point": [32.848132, -116.805901]
                        },
                        "weather": {
                            "repeat_values": {
                                "wind_direction": 180,
                                "wind_speed": 5,
                                "relative_humidity": 5,
                                "temperature": 70
                            }
                        },
                        "fuel_moisture": {
                            "one_hr": 3, 
                            "ten_hr": 4, 
                            "hundred_hr": 6,
                            "live_herb": 5,
                            "live_woody": 60
                        },
                        "webhook": {
                            "url": "https://wifire-webhook.nrp-nautilus.io/webhook",
                            "request_id": "2"
                        }
        }
        return defaultParams

    def getEnsembleLatLongList(self,latLong,count=0,dx=0.01):
        returnList = []
        returnList.append(latLong)
        for i in range(1,count):
            returnList.append([latLong[0] + dx*i, latLong[1] + dx*i])
        return returnList

    def setParamDict(self,params):
        #Change this to iterate through each dictionary key and assing it to farsiteParams
        self.farsiteParams['ignition']['point'] =  params['ignition']['point']
        self.farsiteParams['webhook']['request_id'] = params['webhook']['request_id']

    def launchFarsiteModel(self,params):
        self.setParamDict(params)
        r = requests.request('POST',self.proxyUrl,headers=self.headers,json=self.farsiteParams)
        if r.status_code != 200:
            sys.exit('Error from proxy endpoint: '+ str(r.text))
        return r
