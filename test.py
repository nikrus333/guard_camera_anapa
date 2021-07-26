from __future__ import print_function, division
import unittest
import cv2
from onvif2 import ONVIFCamera, ONVIFError
import requests



DEBUG = False

class Cam():
    def __init__(self) :
        CAM_HOST = '192.168.88.253'
        CAM_PORT = 80
        CAM_USER = 'admin'
        CAM_PASS = 'Aa1234567890'
        self.mycam = ONVIFCamera(CAM_HOST, CAM_PORT, CAM_USER, CAM_PASS)
        self.media2_service = self.mycam.create_media2_service()
        self.profiles = self.media2_service.GetProfiles()[0]
        self.ptz = self.mycam.create_ptz_service()
        self.ptzConfigurationsList = self.mycam.ptz.GetConfigurations()
        self.ptzConfiguration = self.ptzConfigurationsList[0]
        self.request = self.ptz.create_type('GetConfigurationOptions')

# set profile token
        self.requestPtzStatus                = self.ptz.create_type('GetStatus')
        self.requestPtzStatus.ProfileToken   = self.profiles.token
        self.status                          = self.ptz.GetStatus(self.requestPtzStatus)

        self.position = { }
        self.position['x']       = self.status.Position.PanTilt.x
        self.position['y']       = self.status.Position.PanTilt.y
        self.position['z']       = self.status.Position.Zoom.x
        self.o = self.media2_service.create_type('GetStreamUri')
        self.o.ProfileToken = self.profiles.token
        self.o.Protocol = 'RTSP'
        self.uri = self.media2_service.GetStreamUri(self.o)
        self.cap = cv2.VideoCapture('rtsp://admin:Aa1234567890@192.168.88.253/Streaming/Channels/101?transportmode=unicast&profile=Profile_1')
        self.dic = {'token': self.profiles.token,
                'rtsp': self.uri}

    def read_data(self):
        self.status                          = self.ptz.GetStatus(self.requestPtzStatus)
        self.position['x']       = self.status.Position.PanTilt.x
        self.position['y']       = self.status.Position.PanTilt.y
        self.position['z']       = self.status.Position.Zoom.x
        mass = [0, 0, 0]
        mass[0] = self.position['x'] * 180   #to do krasivo sdelat
        mass[1] = self.position['y'] * 180 / 3.14 + 53.8
        mass[2] = self.position['z']
        return (mass)

if __name__ =="__main__":
	cam = Cam()
	while True:
	    print(cam.read_data())


# z = 1 0.0
# 2 0.042857
# 5 0.13
# 10 0.28
# 15 0.41
# 18 0.511143
# 26 0.722857
# 30 0.842857
# 36 1