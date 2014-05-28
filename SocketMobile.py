#!SocketForMobile.py
import socket
import doubanFM
import thread
class FMSocketServer:
	"""A Socket Server provide control API"""
	def __init__(self, ):
		self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM);
		host = socket.gethostbyname(socket.gethostname())
		
		self.socket.bind((host,5007))
		self.socket.listen(100);
		self.doubanFM = doubanFM.DouBanFMOnBerray()
		thread.start_new_thread(self.doubanFM.playMusicFormFM, ("zq54zquan@gmail.com","7991205aa"))
	def startServer(self):
		while (1):
			(conn,addr) = self.socket.accept()
			print(addr);
			thread.start_new_thread(self.handle, (conn,))
	
	def handle(self,conn):
		data = conn.recv(1024);
		while (data!=None):
			if data.encode("utf-8") == "1" or str(data)=="1":
				print("===========next");
				self.doubanFM.stop();
				conn.sendall(data);
			data = conn.recv(1024);
		# conn.close();
		# self.startServer()


fmSocket = FMSocketServer()
fmSocket.startServer()