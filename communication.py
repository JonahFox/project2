# Jonah Fox
# 11/1/2022
# Project 2
# communication.py facilitates communication between a client, and a server. Allows the user to enter
# a message and an IP address, and sends the message if the server is accepting messages.
# Proper error handling for things like: invalid IP address, message timeout, etc.

import socket

# Constant for the port that was opened within my PC's firewall.
PORT = 65432

# Constant message that the server will send to the client to confirm message was received.
ACK_TEXT = "#<<END>>#"


def do_option(option):
    '''Respond to a menu option by calling the appropriate function. If an option 
    that is < 0 and > 2  or not an int is specified, an error message will be printed.
    Parameters:
        option : (int) The selected option.'''
    if option == '1':  # If user enters 1, execute the send_message() function.
        send_message()
    # If user enters 2, execute the receive_message() function.
    elif option == '2':
        receive_message()
    elif option == '0':  # If the user enters 0, exit the program.
        exit
    else:  # Else statement to handle all other options throwing an error if anything other than 0, 1, 2 is entered.
        print("\nError, invalid input. \n")


def menu():
    '''Helper function used to print out the menu
    Parameters:
    '''
    print("===The Python Communicator===")
    print("1) send message ")
    print("2) receive message ")
    print("0) exit ")


def main():
    '''Run the program by asking the user to enter an option and then passes that option
    to our do_option function '''
    menu()
    option = input("Enter Option: ")
    while option != "0":
        do_option(option)
        menu()
        option = input("Enter Option: ")
    print("Goodbye!")


def validate_ip_address(addr):
    '''This is a helper function used to validate an IP address is the correct format,
    It checks that the ip address has four periods, and makes sure that the number range 
    is between 0-255.
    Parameters:
        addr :  This is what the user enters when asked for an IP address.'''
    parts = addr.split(".")  # Splitting the address at the "."

    if(len(parts)) != 4:  # If parts does not have 4 periods, return False.
        print("IP address {} is not valid".format(addr))
        return False

    for part in parts:
        # Validates that the things entered are integers.
        if not isinstance(int(part), int):
            print("IP address {} is not valid".format(addr))
            return False

        # Validates the numbers are between 0 and 255 just like an IP.
        if int(part) < 0 or int(part) > 255:
            print("IP address {} is not valid".format(addr))
            return False
    # Print that the IP is valid and return true.
    print("IP address {} is valid".format(addr))
    return True


def gather_ip():
    '''This is a small helper function used to gather the destination IP from the sender. 
    Parameters:
        recipient_ip :  This is what the user enters when asked for an IP address.
    Returns:
        Returns recipient_ip for use in other functions.'''
    recipient_ip = input("Enter Recipient IP: ")
    return recipient_ip


def send_message():
    '''This function is used to gather the message, the IP, and attempt to send a message to the
    supplied IP address. If the message fails to send, timeout with grace. 
    Parameters:
        msg :  The message that the person wants to send.
        loop : Used to hold a boolean value for our while loop.
        recipient_ip : This calls our gather_ip() helper function to gather the IP address'''
    msg = input("Enter Message (max 4096 characters): ")
    if len(msg) > 4096:
        print("message is too long. (Max characters 4096)")
    loop = True
    recipient_ip = gather_ip()  # Gather initial IP from the user.
    while loop:
        # using our validate_ip_address function, to check validitity
        if validate_ip_address(recipient_ip) is False:
            # If it is false, we reassign the recipient_ip variable to our gather_ip function to gather it again.
            recipient_ip = gather_ip()
        else:
            # loop is set to false once a valid IP has been entered.
            loop = False
            try:  # Try except block for sending our message to the recipient.
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(30.0)  # Timeout of 30 seconds applied.
                    # Trying to connect to our supplied IP/Port
                    s.connect((recipient_ip, PORT))
                    # Setting timeout to none once we have connected successfully.
                    s.settimeout(None)
                    s.sendall(msg.encode("utf-8"))
                    print("Sending.")
                    data = s.recv(1024)
                    print("\nMessage sent successfully.\n")
            except:
                print("\nThe message failed to send... Returning to menu..\n")


def receive_message():
    '''This is a helper function used to validate an IP address is the correct format,
    It checks that the ip address has four periods, and makes sure that the number range 
    is between 0-255.
    Parameters:
        ALL_IP :  An empty string used as a parameter when binding, connecting to any available IP.'''
    print("Waiting for message on port", PORT)
    ALL_IP = ""
    # Initiating our socket as s.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ALL_IP, PORT))  # Binding to any IP, and a specific port.
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
                    print(data.decode(), end="#")
                    print("\nEnd of message.\n")
                conn.sendall(ACK_TEXT.encode("utf-8"))


if __name__ == "__main__":
    main()
