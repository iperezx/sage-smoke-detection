import os
import requests

_authURL = 'https://hotshot.sdsc.edu/pylaski/auth'
# _proxyUrl = 'https://wifire-api-proxy.nautilus.optiputer.net'
_proxyUrl = 'https://wifire-api-proxy.nrp-nautilus.io'

class Trigger:

    def __init__(self, 
                 model_type,
                 execute,
                 authURL=_authURL,
                 proxyUrl=_proxyUrl,
                 ):
        authToken = self.getAuthToken(authURL)
        print("")
        print("authToken")
        print(authToken)
        print("")
        self.headers = {'content-type': "application/json",
                        'authorization': 'Bearer ' + authToken['token']}
        self.farsiteParams = self.getDefaultParams()
        self.proxyUrl = proxyUrl
        self.do_trigger = self.predictFire(execute)
        if self.do_trigger:
            self.trigger()


    def predictFire(self, execute):
        image_preds, _, _ = execute.inference_results
        return True in image_preds


    def trigger(self):
        """
        TODO: Implement this method
        """
        print("Triggering")
        counter = 0
        siteLatLong = [32.848132, -116.805901]
        ensembleLatLongList = self.getEnsembleLatLongList([siteLatLong[0],siteLatLong[1]])
        params = self.getDefaultParams()
        for latLong in ensembleLatLongList:
            params['ignition']['point'] =  latLong
            params['webhook']['request_id'] = str(counter)
            returnStatus = self.launchFarsiteModel(params)
            print("Return status:")
            print(returnStatus)


    def getEnsembleLatLongList(self, latLong, count=0, dx=0.01):
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
        print("Farsite Params")
        print(self.farsiteParams)
        r = requests.request('POST', self.proxyUrl, headers=self.headers, json=self.farsiteParams)
        # r = requests.request('POST', self.proxyUrl, headers=self.headers, json={}, verify=False)
        print('text', r.text)
        print('status_code', r.status_code)
        print('json', r.json())
        return r.text


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
        return authToken


    def getDefaultParams(self):
        defaultParams = {"hours": 1,
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
                            "request_id": "0"
                        }
        }
        return defaultParams

