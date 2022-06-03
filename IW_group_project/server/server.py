import socket
import os
import base64
import time

# Establishing connection
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 12000  # Port to listen on (non-privileged ports are > 1023)


# Uploading to the server from the client
def download_from_client():
    filename = connect.recv(1024).decode()
    f = open(filename, 'wb')
    file_chunk = connect.recv(2048)

    while file_chunk:
        f.write(file_chunk)
        file_chunk = connect.recv(2048)

    print('File downloaded from client.')
    f.close()


# Download to the server from the client
def upload_to_server():
    filename = connect.recv(1024).decode()
    # Choosing a file
    with open(filename, 'rb') as f:
        print("File opened!")
        while True:
            data = base64.b64encode(f.read(1024))
            if not data:
                print('File upload complete.')
                break
            connect.send(data)
            time.sleep(0.00001)

    f.close()


def file_list():
    filelist = [f for f in os.listdir('.') if os.path.isfile(f)]
    connect.send(str(filelist).encode())


def chat_feature():
    # Since the user has chosen the chat option, we want to send the entire chat first.
    with open('chatlog.txt', 'rb') as chat:
        print('Sending the chatlogs to the client')
        while True:
            data = base64.b64encode(chat.read(1024))
            if not data:
                print('File upload complete.')
                break
            connect.send(data)
            time.sleep(0.00001)
    chat.close()
    print('Reaching here!!')
    receivedMsg = connect.recv(10)
    print(receivedMsg)
    # with open('chatlog.txt', 'w') as chat:
    #     while True:
    #         receivedMsg, address = udp.recvfrom(1024)
    #         receivedMsg = receivedMsg.decode().split('.!?')
    #         if receivedMsg[1] == '!q':
    #             chat.close()
    #             break
    #         else:
    #             chat.write(f'[{receivedMsg[0]}]: ' + receivedMsg[1])
    # chat.close()


def modes(option):
    if option == '1':
        file_list()
    elif option == '2':
        download_from_client()
    elif option == '3':
        upload_to_server()
    elif mode == '4':
        chat_feature()
    elif mode == '5':
        # check_login()
        print('Logout procedure initiated.')


def check_login(user, pas):
    # check the credentials in the credentials.txt file
    print('Checking credentials.')
    file = open('credentials.txt', 'r')
    while True:
        line = file.readline()
        if not line:
            break
        # There must be a better way of checking if the username and passwords are valid.
        if user in line and pas in line:
            file.close()
            connect.send('Credentials Accepted'.encode())
            return
    file.close()
    connect.send('Credentials Rejected'.encode())
    check_login(connect.recv(1024).decode(), connect.recv(1024).decode())


# Establishing a TCP connection with client.
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind((HOST, PORT))
tcp.listen()

# Establishing a UDP connection with client.
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
udp.bind((HOST, 12001))

print("Server ready to send")
connect, addr = tcp.accept()

# Login functionality
username = connect.recv(1024).decode()
password = connect.recv(1024).decode()
check_login(username, password)

mode = connect.recv(1024).decode()
modes(mode)
tcp.close()
