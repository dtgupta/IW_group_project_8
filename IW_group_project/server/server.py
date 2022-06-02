import socket
import os
import base64
import time

# Establishing connection
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 12001  # Port to listen on (non-privileged ports are > 1023)


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
                print('File download complete.')
                break
            connect.send(data)
            time.sleep(0.00001)

    f.close()


def file_list():
    filelist = [f for f in os.listdir('.') if os.path.isfile(f)]
    connect.send(str(filelist).encode())


def modes(option):
    if option == '1':
        file_list()
    elif option == '2':
        download_from_client()
    elif option == '3':
        upload_to_server()
    # elif mode == '4':

    elif mode == '5':
        # check_login()
        print('Logout procedure initiated.')


def check_login(user, pas):
    # check the credentials in the credentials.txt file
    print('Checking credentials.')
    file = open('credentials.txt', 'r')
    while True:
        line = file.readline()[:-1]
        if not line:
            break
        # There must be a better way of checking if the username and passwords are valid.
        cred = line.split(",", 2)
        print(cred)
        if user == cred[0] and pas == cred[1]:
            file.close()
            connect.send('Credentials Accepted'.encode())
            return True
    file.close()
    connect.send('Credentials Rejected'.encode())
    return False
    # check_login(connect.recv(1024).decode(), connect.recv(1024).decode())


# Establishing connection with client.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print("Server is operational")
connect, addr = s.accept()
# Login functionality
tryLog = True
while tryLog: 
    usernamePass = (connect.recv(1024).decode()).split(",")
    if (usernamePass[0] == ""):
        s.close()
        quit()
    username, password = usernamePass[0], usernamePass[1] 
    if check_login(username, password):
        break

mode = connect.recv(1024).decode()
print(mode)
modes(mode)
s.close()
