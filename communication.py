import socket
#65432 port 
#192.168.1.8

SERVER = ""
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(30.0)
    s.connect((SERVER, PORT))
    s.settimeout(None)
    s.sendall(b"Hello, world")
    data = s.recv(1024)

VM_IP = ""
ALL_IP = ""
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
    s.bind((ALL_IP, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn: 
        print(f"Connected by {addr}")
        exit = False
        while not exit: 
            data = conn.recv(1024)
            if not data: 
                exit = True
            else: 
                print(data.decode(), end="#")
            conn.sendall(data)