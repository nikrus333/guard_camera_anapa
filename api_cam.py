from PIL import Image, ImageTk
import tkinter as tk
import cv2
import test
import algoritm
import create_json
import map
import server_data


class Application():
    def __init__(self):
        """ Initialize application which uses OpenCV + Tkinter. It displays
            a video stream in a Tkinter window and stores current snapshot on disk """
        self.cam = test.Cam()
        self.algoritm = algoritm.CoordAlgoritm()
        self.map =map.GetMap()
        self.create_file = create_json.CreteJsonFile()

        #self.server = server_data.ServerUDP('1')
        #self.server.start()
        self.vs = self.cam.cap # capture video frames, 0 is your default video camera
        self.current_image = None  # current image from the camera
        
        self.root = tk.Tk()  # initialize root window
        self.root.title("dron.exe")  # set window title
        # self.destructor function gets fired when the window is closed
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry('1920x1080')
        self.panel = tk.Label(self.root)  # initialize image panel
        self.panel.pack(padx=10, pady=10)
        self.panel.bind('<Motion>', self.motion)
        #name_label.grid(row=0, column=0, sticky="w")
        btn = tk.Button(self.root, text="Start dron", command=self.take_snapshot)
        self.panel.bind("<Button-2>",self.fun)
        btn.pack(fill="both", expand=True, padx=10, pady=10)
        self.coord_actual = [None, None]
        self.cord_final_mouse = [None, None]
        self.video_loop()
        #self.serve_loop()

    def video_loop(self):
        """ Get frame from the video stream and show it in Tkinter """
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            frame = cv2.resize(frame, (1600, 900))
            frame = cv2.circle(frame,(800, 450), 5, (255, 0, 0), 2, 8, 0)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image
            )  # convert image for tkinter
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image
            #self.server.action_server()
        self.root.after(1, self.video_loop)
        #print(self.coord)  # call the same function after 30 milliseconds
    def motion(self, event):
        self.coord_actual[0], self.coord_actual[1] = event.x, event.y
        #print('{}, {}'.format(self.coord_actual[0], self.coord_actual[1]))
       

    def take_snapshot(self):
        print('_____________')
        print(self.cam.read_data())
        print('_____________')
        _ = self.algoritm.solution(self.cam.read_data(), self.cord_final_mouse) # method solution_mouse or solution
        #self.server.send_client(str(_))
        self.create_file.create(_)
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
              
    def fun(self, event):
        self.cord_final_mouse = self.coord_actual
        
    def destructor(self):
        """ Destroy the root object and release all resources """
        print("[INFO] closing...")
        self.root.destroy()
        self.vs.release()  # release web camera
        cv2.destroyAllWindows()  # it is not mandatory in this application


print("[INFO] starting...")
pba = Application()
pba.root.mainloop()

