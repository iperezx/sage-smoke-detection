import os
import requests
from requests.exceptions import HTTPError

class cameras:
    def __init__(self,hpwrenUrl):
        self.hpwrenUrl = hpwrenUrl
        self.setHPWRENCamsData()

    def setHPWRENCamsData(self):
        try:
            self.requestData = requests.get(self.hpwrenUrl)
            self.requestData.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

        self.hpwrenCams = self.requestData.json()


    def getImageURL(self, cameraType=0,siteID=0):
        hpwrenCamsAtSite = self.hpwrenCams["features"][siteID]
        hpwrenCamAtSiteCamType = hpwrenCamsAtSite["properties"]["latest-images"][cameraType][0]
        descriptionName = hpwrenCamsAtSite["properties"]["description"]['name']

        colorVal = hpwrenCamAtSiteCamType['color']
        diffVal = hpwrenCamAtSiteCamType['diff']

        colorType = 'Color' if colorVal else 'Monochrome'
        diffType = 'Difference' if diffVal else 'Original'

        # check that the camera that the user picked is color and non-diff
        # the model only supports color images and original type
        if colorVal and not diffVal:
            imageURL = hpwrenCamAtSiteCamType["image"]
            direction = hpwrenCamAtSiteCamType['direction'].capitalize()
            description = descriptionName + ' ' + direction + ' ' + colorType + ' ' + diffType
        else:
            imageURL = 'None'
            description = 'None'

        return imageURL,description
