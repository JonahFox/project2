import socket
SERVER = "192.168.1.9"
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), PORT))
msg = s.recv(1024)
print(msg.decode("utf-8"))
