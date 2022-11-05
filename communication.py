import socket
# 65432 port
# 192.168.1.8

PORT = 65432
ACK_TEXT = "#<<END>>#"


def do_option(option):
    '''Respond to a manu option by calling the appropriate function. If an option 
    that is <= 0 and > 7  or not an int is specified, an error message will be printed.
    Parameters:
        option : (int) The selected option.'''
    if option == '1':  # Make keys
        send_message()
    elif option == '2':
        receive_message()
    else:
        print("Error, invalid input ")


def menu():
    print("===The Python Communicator===")
    print("1) send message ")
    print("2) receive message ")
    print("0) exit ")


def main():
    '''Run the program by asking the user to enter ansd option and then by acting 
    on that optioin with the enter_option command.'''
    menu()
    option = input("Enter Option: ")
    while option != "0":
        do_option(option)
        menu()
        option = input("Enter Option: ")

    print("Goodbye!")


def validate_ip_address(addr):
    parts = addr.split(".")

    if(len(parts)) != 4:
        print("IP address {} is not valid".format(addr))
        return False

    for part in parts:
        if not isinstance(int(part), int):
            print("IP address {} is not valid".format(addr))
            return False

        if int(part) < 0 or int(part) > 255:
            print("IP address {} is not valid".format(addr))
            return False
    print("IP address {} is valid".format(addr))
    return True


def gather_ip():
    recipient_ip = input("Enter Recipient IP: ")
    return recipient_ip


def send_message():
    msg = input("Enter Message (max 4096 characters): ")
    loop = True
    recipient_ip = gather_ip()
    while loop:
        if validate_ip_address(recipient_ip) is False:
            recipient_ip = gather_ip()
        else:
            loop = False
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(30.0)
                    s.connect((recipient_ip, PORT))
                    s.settimeout(None)
                    s.sendall(msg.encode("utf-8"))
                    print("Sending.")
                    data = s.recv(1024)
                    print("\nMessage sent successfully.\n")
            except:
                print("\nThe message failed to send... Returning to menu..\n")


def receive_message():
    print("Waiting for message on port", PORT)
    ALL_IP = ""
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
                    print("Message successfully sent.")
                    print("Message:\n")
                    print(data.decode())
                    print("\nEnd of message.\n")
                conn.sendall(ACK_TEXT.encode("utf-8"))


if __name__ == "__main__":
    main()
