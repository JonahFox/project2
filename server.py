import socket

VM_IP = "192.168.1.9"
ALL_IP = ""
PORT = 65432
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), PORT))
s.listen(5)

while True:
    clientsocket, addr = s.accept()
    print(f"Connection from {addr} has been established!")
    clientsocket.send(bytes("Welcome to the server ", "utf-8"))





# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
#     s.bind((ALL_IP, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn: 
#         print(f"Connected by {addr}")
#         exit = False
#         while not exit: 
#             data = conn.recv(1024)
#             if not data: 
#                 exit = True
#             else: 
#                 print(data.decode(), end="#")
#             conn.sendall(data)