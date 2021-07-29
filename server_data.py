
import socket
from threading import Thread
import time
class ServerUDP(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        self.localIP     = "192.168.52.101"
        self.localPort   = 7776
        self.bufferSize  = 1024
        self.msgFromServer       = "Hello UDP lient"
        self.message = None
        self.address = None 
        self.err = None
        self.bytesToSend         = str.encode(self.msgFromServer)
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((self.localIP, self.localPort))
        self.UDPServerSocket.settimeout(2)
        print("UDP server up and listening")
# Listen for incoming datagrams
    def run(self):
        while True:
            try:
                z = 0
                #self.bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
                #self.message = self.bytesAddressPair
                #clientMsg = "Message from Client:{}".format(self.message)
                #clientIP  = "Client IP Address:{}".format(self.address)
                #time.sleep(1)
            except socket.timeout as err:
                self.err = err
    
    def send_client(self, data_coord):
        self.msgFromServer       = data_coord
        self.bytesToSend         = str.encode(self.msgFromServer)
        self.address             = ("192.168.52.244", 7777)
        self.UDPServerSocket.sendto(self.bytesToSend, self.address)

def main():
    server = ServerUDP()
    while True:
        server.action_server()
        print("send message")

if __name__ == "__main__":
    main()