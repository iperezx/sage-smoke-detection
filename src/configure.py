import abc
import hpwren
from pathlib import Path

class CameraDeviceInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_metadata') or NotImplemented)

    @abc.abstractmethod
    def get_metadata(self):
        """Get camera devices metadata"""
        raise NotImplementedError

class CameraDeviceBase(CameraDeviceInterface):
    def __init__(self):
        self.camera_src = ''
        self.server_name = ''
        self.image_url = ''
        self.description = ''
    
    def get_metadata(self):
        return {
                    'camera_src': self.camera_src,
                    'server_name': self.server_name,
                    'image_url': self.image_url,
                    'description': self.description
                }

class Recorded_MP4(CameraDeviceBase):
    def __init__(self):
        self.sample_mp4 = '20190610-Pauma-bh-w-mobo-c.mp4'
        self.camera_src = Path(self.sample_mp4)
        self.server_name = self.sample_mp4
        self.image_url = self.sample_mp4
        self.description = 'Pre-recorded video'
    
class Camera_Device(CameraDeviceBase):
    def __init__(self, camera_endpoint):
        self.camera_src = camera_endpoint
        self.server_name = camera_endpoint
        self.imageURL = camera_endpoint
        self.description = f'{camera_endpoint} Camera on Device'

class Hpwren(CameraDeviceBase):
    def __init__(self,camera_id,site_id):
        self.camera_id = camera_id
        self.site_id = site_id
        self.server_name = 'HPWREN Camera'
        self.hpwrenUrl = "https://firemap.sdsc.edu/pylaski/"\
            "stations?camera=only&selection="\
            "boundingBox&minLat=0&maxLat=90&minLon=-180&maxLon=0"
        camObj = hpwren.cameras(self.hpwrenUrl)
        self.image_url,self.description = camObj.getImageURL(camera_id,site_id)
        self.camera_src = self.image_url