import math
# 44°54'12.2"N 37°18'49.4"E
class CoordAlgoritm():
    def __init__(self, angle_cam = [70, 80, 0], coord_mouse = [600, 450], scale_windows = 1):
        self.H_CAM_ = 6.5 #высота камеры над уровнем моря
        self.angle_cam = angle_cam
        self.viewing_angle_cam_gorizontal = 56.1 /2
        self.viewing_angle_cam_vertical = 33.4 / 2
        self.coord_mouse_windows = coord_mouse
        self.cam_coord_N = 44.901561
        self.cam_coord_E = 37.316337
        self.azimut_ahgle_cam = 58.1041
        self.zero_angle_cam = 90 - self.azimut_ahgle_cam

    def gradus_to_radian(self, grad):
        return grad / 180 * math.pi
    def radian_to_gradus(self, radian):
        return radian * 180 / math.pi

    def g_to_m(self, b, lat, lon):
        b = self.gradus_to_radian(b)
        x = lat * 111138
        y = lon * math.cos(b) * 111138
        return [x, y]
    def m_to_g(self, b, x, y, lat, lon):
        b = self.gradus_to_radian(b)
        lat = x /  (math.sin(b) * 111138)
        lon = y / (math.cos(b) * 111138)
        return [lat, lon]
    #def azimut(self, llat1 = 77.1539, llong1 = -120.398, llat2 = 77.1804, llong2 = 129.55):
       # rad = 6372795
       # lat1 = llat1*math.pi/180


    def get_ahgle_cam(self, x2, y2, x1, y1):
        dx = x2 - x1
        dy = y2 - y1
        if dx > 0:
            result = (3.1415926 / 2) - math.atan(dy / dx)
        else:
            if dx < 0:
                result = (3.1415926 * 1.5) - math.atan(dx / dy)
            else:
                if dy > 0:
                    result = 0
                    



    def get_directional_angle(self, x2, y2, x1, y1):
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0:
            if dy > 0:
                return 0
            if dy < 0:
                return self.gradus_to_radian(180)
        if dy == 0:
            if dx > 0:
                return self.gradus_to_radian(90)
            if dx < 0:
                return self.gradus_to_radian(270)
        if dx > 0 and dy > 0:
            i_quarter = 1
        if dx > 0 and dy < 0:
            i_quarter = 2
        if dx < 0 and dy < 0:
            i_quarter = 3
        if dx < 0 and dy > 0:
            i_quarter = 4
        
        dx = abs(dx)
        dy = abs(dy)
        if dx == 0:
            dy = 0.00000000001
        if dy == 0:
            dy = 0.00000000001
        f_angle = math.atan(dx / dy)
        if i_quarter == 1:
            return self.gradus_to_radian(90) - f_angle
        else:
            if i_quarter == 2:
                return self.gradus_to_radian(90) - self.gradus_to_radian(360) - f_angle
            else:
                if i_quarter == 3:
                    return self.gradus_to_radian(90) - self.gradus_to_radian(180) + f_angle
                else:
                    if i_quarter == 4:
                        return self.gradus_to_radian(90) - self.gradus_to_radian(180) - f_angle
                    else:
                        return 0


    def coordinat(self, x1, y1, x2, y2, dist_, ugol, vugol):
        buf = self.get_directional_angle(x2, y2, x1, y1)
        buf2 = self.gradus_to_radian(ugol) + (self.gradus_to_radian(90) - buf)
        buf = buf2
        RAS = self.gradus_to_radian(vugol)
        x_out = math.cos(buf) * (dist_ + (dist_ * RAS)) + x2
        y_out = math.sin(buf) * (dist_ + (dist_ * RAS)) + y2
        return [x_out, y_out]

    def angle_cam_azimut(self, angle_cam, b_catet):
        # p 0 - camera = 58.5 azimut
        # 45.5641 
        print("angle_strar", angle_cam[0])
        
        #angle = 58.5 - angle_cam[0] 
        #shir = math.cos(self.gradus_to_radian(angle)) *  b_catet
        #dolgota = math.sin(self.gradus_to_radian(angle)) *  b_catet
        if angle_cam[0] >= - self.zero_angle_cam:
            angle = 58.5 - angle_cam[0] 
            print("angle_new", angle)
            shir = math.cos(self.gradus_to_radian(angle)) *  b_catet
            dolgota = math.sin(self.gradus_to_radian(angle)) *  b_catet
            new_shir = self.cam_coord_N + (shir * 0.00000000001 / 0.000001111 )
            new_dologota = self.cam_coord_E - (dolgota * 0.0000001 / 0.007876)
        if angle_cam[0] < - self.zero_angle_cam:
            angle = - self.zero_angle_cam - angle_cam[0]
            print("angle_new", angle)
            shir = math.sin(self.gradus_to_radian(angle)) *  b_catet
            dolgota = math.cos(self.gradus_to_radian(angle)) *  b_catet
            new_shir = self.cam_coord_N - (shir * 0.00000000001 / 0.000001111 )
            new_dologota = self.cam_coord_E - (dolgota * 0.0000001 / 0.007876)
        return [new_shir, new_dologota]



    def solution(self, angle_cam,  coord_mouse = [600, 450]):
        self.angle_cam = angle_cam
        self.coord_mouse_windows = coord_mouse
        # b_catet растояние от основания вышки до точки на воде, куда падает луч из центра камеры
        b_catet = self.H_CAM_ * math.tan(self.gradus_to_radian(self.angle_cam[1]))
        # x_coord y_coord координаты точки на воде, куда падает луч из центра камеры
        x_coord = math.sin(self.gradus_to_radian(self.angle_cam[0])) * b_catet
        y_coord = math.cos(self.gradus_to_radian(self.angle_cam[0])) * b_catet
        
        coord_ = self.angle_cam_azimut(angle_cam, b_catet)
        return coord_

    def solution_mouse(self, angle_cam = [1, 85, 0],  coord_mouse = [800, 450]):
        self.angle_cam = angle_cam
        print('algoritm ',self.angle_cam[0])
    
        if coord_mouse[0] <= 800:
            self.angle_cam[0] = self.angle_cam[0] - (self.viewing_angle_cam_gorizontal * coord_mouse[0] / 800)
        if coord_mouse[0] > 800:
            self.angle_cam[0] =self.angle_cam[0] + (self.viewing_angle_cam_gorizontal * coord_mouse[0] / 1600)
        if coord_mouse[1] <= 450:
            self.angle_cam[1] =self.angle_cam[1] - (self.viewing_angle_cam_vertical * coord_mouse[1] / 450)
        if coord_mouse[1] > 450:
            self.angle_cam[1] =self.angle_cam[1] + (self.viewing_angle_cam_vertical * coord_mouse[1] / 900)
        self.coord_mouse_windows = coord_mouse
        # b_catet растояние от основания вышки до точки на воде, куда падает луч 
        b_catet = self.H_CAM_ * math.tan(self.gradus_to_radian(self.angle_cam[1]))
        # x_coord y_coord координаты точки на воде, куда падает луч 
        x_coord = math.cos(self.gradus_to_radian(self.angle_cam[0])) * b_catet
        y_coord = math.sin(self.gradus_to_radian(self.angle_cam[0])) * b_catet
        return [x_coord, y_coord]