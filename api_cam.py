import os
from settings import Settings
from tkinter.constants import BOTH
basedir = os.path.abspath(os.path.dirname(__file__))

from PIL import Image, ImageTk
import tkinter as tk
import cv2
from tkinter import Frame, messagebox, filedialog
from tkinter.ttk import Notebook
import threading
import json
from importlib import reload

import algoritm
import create_json
import map
import server_data
import settings
'''
class Cam():
    def __init__(self) :
        CAM_HOST = '192.168.88.253'
        CAM_PORT = 80
        CAM_USER = 'admin'
        CAM_PASS = 'Aa1234567890'
        self.mycam = client.ONVIFCamera(CAM_HOST, CAM_PORT, CAM_USER, CAM_PASS)
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
        mass[0] = self.position['x'] * 180   # преобразование координат камеры в углы 
        mass[1] = self.position['y'] * 180 / 3.14 + 52.8014
        mass[2] = self.position['z']
        return (mass)
'''
class Application():
    def init_api_wid(self):
        self.flaf_detection_dot = False #flag program

        self.root = tk.Tk()  # initialize root window
        self.root.title("Система мониторинга")  # set window title
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry('1920x1080')
        self.tabs_control = Notebook(self.root)
        self.tab_1 = Frame(self.tabs_control)
        self.tabs_control.add(self.tab_1, text='Наблюдение')
        self.tab_2 = Frame(self.tabs_control)
        self.tabs_control.add(self.tab_2, text='Настройка')
        self.tabs_control.pack(fill=BOTH)
        self.panel = tk.Label(self.tab_1)  # initialize image panel
        self.panel.pack(padx=10, pady=10)
        self.panel.bind('<Motion>', self.motion)
        btn = tk.Button(self.tab_1, width=30, text="отправить координаты", bd=1, font="Arial 14", command=self.sendCord)
        btn1 = tk.Button(self.tab_1, width=30, text="        запуск дрона         ", bd=1, fg="red", font="Arial 14", command=self.startDron)
        self.panel.bind("<Button-2>",self.fun)
        btn_tab_2 = tk.Button(self.tab_2, width=30, text="Начать калибровку", bd=1, font="Arial 14", command=self.calibrate)
        btn_tab_2_file = tk.Button(self.tab_2, width=30, text="Загрузить файл конфигурации", bd=1, font="Arial 14", command=self.open_file)
        btn.pack()
        btn1.pack()
        btn_tab_2.pack()
        btn_tab_2_file.pack()
        self.coord_actual = [None, None]
        self.cord_final_mouse = [None, None]
        server_udp = threading.Thread(target = self.server.run)
        server_udp.start()
        self.video_loop()

        
        

    def __init__(self):
        """ Initialize application which uses OpenCV + Tkinter. It displays
            a video stream in a Tkinter window and stores current snapshot on disk """
       
        self.setting = settings.Settings()

        ##self.cam = Cam()


        self.algoritm = algoritm.CoordAlgoritm()
        self.algoritm.H_CAM_ = self.setting.hight
        self.algoritm.azimut_ahgle_cam = self.setting.azimut_ahgle_cam

        self.map = map.GetMap()
        #self.create_file = create_json.CreteJsonFile()
        self.server = server_data.ServerUDP('1')
        self.vs = cv2.VideoCapture(0)   ##self.cam.cap # capture video frames, 0 is your default video camera
        self.current_image = None  # current image from the camera
        self.init_api_wid()
        
    def video_loop(self):
        """ Get frame from the video stream and show it in Tkinter """
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            frame = cv2.resize(frame, (1600, 900))
            if self.flaf_detection_dot == True:
                color = (0, 0, 255)
                radius = 10
            else:
                color = (255, 0, 0)
                radius = 5
            frame = cv2.circle(frame,(800, 450), radius, color, 2, 8, 0)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image
        self.root.after(1, self.video_loop)

    def motion(self, event):
        self.coord_actual[0], self.coord_actual[1] = event.x, event.y
        
    def startDron(self):
        data = "#start"
        MsgBox = messagebox.askquestion ('Запуск дрона','ЗАПУСТИТЬ ДРОН?',icon = 'warning')
        if MsgBox == 'yes':
            self.server.send_client(data)
            self.flaf_detection_dot = False
        else:
            mesbox =messagebox.showinfo(title="Дрон", message="Запуск дрона отменен")

    def sendCord(self):
        if self.flaf_detection_dot == True:
            ##_ = self.algoritm.solution(self.cam.read_data(), self.cord_final_mouse) # method solution_mouse or solution
            _ = [43, 33]
            
            #self.create_file.create(_)
            string ='#' + str(_[0]) + '#' + str(_[1])
            self.server.send_client(string)
            try:
                self.map.get_map_image(coord_dot_sos = _)
                self.map = Image.open("1.PNG")
                self.maps = ImageTk.PhotoImage(self.map)
                label1 = tk.Label(image = self.maps)
                label1.image_names = 'dzen'
                label1.place(x = 1500, y = 550)
            except Exception:
                print("Ошибка доступа к google api")
            print(_, "solutiom")
        else:
            mesbox =messagebox.showinfo(title="Дрон", message="Целевая точка не определена. Для определения целевой точки используйте колесико мыши")
              
    def fun(self, event):
        self.cord_final_mouse = self.coord_actual
        self.flaf_detection_dot = True
        self.mesbox =messagebox.showinfo(title="Точка определена", message="Точка определена")
        
    def calibrate(self):
         self.mesbox =messagebox.showinfo(title="Dron", message="Калибровка прошла успешно")    

    def open_file(self):
        file_name = filedialog.askopenfilename()
        with open(file_name, "r") as f:
            data = json.load(f)
            self.setting.read_data_from_file(data)
 
    def destructor(self):
        """ Destroy the root object and release all resources """
        print("[INFO] closing...")
        self.server.life = False
        self.root.destroy()
        self.vs.release()  # release web camera
        cv2.destroyAllWindows()  # it is not mandatory in this application


print("[INFO] starting...")
pba = Application()
pba.root.mainloop()