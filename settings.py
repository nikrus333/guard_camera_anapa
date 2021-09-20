import json
class Settings():
    def __init__(self):
        with open("config.json", "r") as f:
            data = json.load(f)

        self.coordinates = data["coordinates"]
        self.hight =  data["hight"]
        self.azimut_ahgle_cam =  data["azimut_ahgle_cam"]
        self.ip_camera =  data["ip_camera"]
        self.login =  data["login"]
        self.password = data["password"]
        self.key_google_maps =   data["key_google_maps"]

    def read_data_from_file(self, data):
        self.coordinates = data["coordinates"]
        self.hight =  data["hight"]
        self.azimut_ahgle_cam =  data["azimut_ahgle_cam"]
        self.ip_camera =  data["ip_camera"]
        self.login =  data["login"]
        self.password = data["password"]
        self.key_google_maps =   data["key_google_maps"]
