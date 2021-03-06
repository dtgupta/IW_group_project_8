import socket
import os
import base64
import time

# Establishing connection
HOST = "127.0.0.1"  # Standard loop back interface address (localhost)
PORT = 12000  # Port to listen on (non-privileged ports are > 1023)


# Uploading to the server from the client
def download_from_client():
    filename = connect.recv(1024).decode()
    f = open(filename, 'wb')
    # file_chunk = connect.recv(2048)

    while True:
        file_chunk = connect.recv(2048)
        if file_chunk.decode() == 'eof':
            print('Download complete.')
            break
        f.write(base64.b64decode(file_chunk))

    print('File downloaded from client.')
    f.close()


# Download to the server from the client
def upload_to_server():
    filename = connect.recv(1024).decode()
    print(filename)
    # Choosing a file
    with open(filename, 'rb') as f:
        print("File opened!")
        while True:
            data = base64.b64encode(f.read(1024))
            if not data:
                print('File upload complete.')
                connect.send('eof'.encode())
                break
            connect.send(data)
            time.sleep(0.0001)

    f.close()
    print('File is closed')


def sbatch_download():
    filelist = [f for f in os.listdir('.') if os.path.isfile(f)]
    connect.send(str(filelist).encode())
    print(len(filelist))

    for i in range(len(filelist)):
        filename = connect.recv(1024).decode()
        f = open(filename, 'rb')
        print("File opened!")
        while True:
            data = base64.b64encode(f.read(1024))
            if not data:
                print('File download complete.')
                connect.send('nextfile'.encode())
                break
            connect.send(data)
            time.sleep(0.00001)

        f.close()
        print('File closed')


def file_list():
    fileList = [f for f in os.listdir('.') if os.path.isfile(f)]
    connect.send(str(fileList).encode())


def chat_feature():
    # Since the user has chosen the chat option, we want to send the entire chat first.
    with open('chatlog.txt', 'rb') as chat:
        print('Sending the chatlogs to the client')
        while True:
            data = base64.b64encode(chat.read(1024))
            if not data:
                connect.send('eof'.encode())
                print('File upload complete.')
                break
            connect.send(data)
            time.sleep(0.00001)
    chat.close()

    # Receiving the chat from the client and appending it to the logs.
    receivedMsg = str(connect.recv(1024), 'UTF-8')
    f = open('chatlog.txt', 'a')
    split = receivedMsg.split('.!?')
    if split[1] != '!q':
        f.write(f'[{split[0]}]: {split[1]}\n')
    f.close()
    # with open('chatlog.txt', 'w') as chat:
    #     while True:
    #         receivedMsg, address = udp.recvfrom(1024)
    #         receivedMsg = receivedMsg.decode().split('.!?')
    #         print(receivedMsg[0] + ": " + receivedMsg[1])
    #         if receivedMsg[1] == '!q':
    #             chat.close()
    #             break
    #         else:
    #             chat.write(f'[{receivedMsg[0]}]: ' + receivedMsg[1])
    # chat.close()


def modes(option):
    ret = False
    if option == '1':
        file_list()
    elif option == '2':
        print('beginning to download from client')
        download_from_client()
    elif option == '3':
        upload_to_server()
    elif mode == '4':
        chat_feature()
    elif mode == '5':
        sbatch_download()
    elif mode == '6':
        print('Logout procedure initiated.')
        ret = True
    return ret


def check_login(user, pas):
    # check the credentials in the credentials.txt file
    print('Checking credentials.')
    file = open('credentials.txt', 'r')
    while True:
        line = file.readline()[:-1]
        if not line:
            break
        # check if the username and passwords are valid.
        cred = line.split(",", 2)
        if user == cred[0] and pas == cred[1]:
            file.close()
            connect.send('Credentials Accepted'.encode())
            return True

    file.close()
    connect.send('Credentials Rejected'.encode())
    return False


# Establishing a TCP connection with client.
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind((HOST, PORT))
tcp.listen()

# Establishing a UDP connection with client.
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
udp.bind((HOST, 12001))

print("Server operational")
connect, addr = tcp.accept()

quitF = False
while not quitF:
    # Login functionality
    while True:
        usernamePass = (connect.recv(1024).decode()).split(",")
        if usernamePass[0] == "":
            print("Connection is over")
            tcp.close()
            exit()
        username, password = usernamePass[0], usernamePass[1]
        if check_login(username, password):
            break

    logout = False
    while not logout:
        mode = connect.recv(1024).decode()
        print('mode should be 2 but is ' + mode)
        logout = modes(mode)
tcp.close()
