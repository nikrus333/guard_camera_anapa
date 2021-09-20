import requests
  
class GetMap():

    def __init__(self):  
# Enter your api key here
        self.api_key = "AIzaSyC7n5-Ua4sSwdVqVk4wzWm-axYxbBpP3kQ"
  
# url variable store url
        self.url = "https://maps.googleapis.com/maps/api/staticmap?"
  
# center defines the center of the map,
# equidistant from all edges of the map. 
  
# zoom defines the zoom
# level of the map
        self.zoom = 17
# get method of requests module
# return response object
    def get_map_image(self, coord_center = [44.902161, 37.3155], coord_anaspas = [44.901561, 37.316337], coord_dot_sos = [44.901561, 37.315537]):
        print('fun_start')
        self.r = requests.get(self.url + 
        "center=" + str(coord_center[0]) + "," + str(coord_center[1])+"&zoom=" +
        str(self.zoom) + "&size=400x600&maptype=satellite&markers=color:blue%7Clabel:Anaspas%7C" + 
        str(coord_anaspas[0]) + "," + str(coord_anaspas[1]) + 
        "&markers=color:blue%7Clabel:dot%7C" + 
        str(coord_dot_sos[0]) + "," + str(coord_dot_sos[1]) +
        "&key=" + self.api_key)
        print('api_work')
# wb mode is stand for write binary mode
        f = open('1.PNG', 'wb')
        print('open_file')
# r.content gives content,
# in this case gives image
        f.write(self.r.content)
        print('write_file')
# close method of file object
# save and close the file
        f.close()
        print('close')

        self.r = None
if __name__ == "__main__":
    pba = GetMap()
    pba.get_map_image()