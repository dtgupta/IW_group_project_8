import socket
import os
import base64

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 12001  # The port used by the server



def download_from_server():
    # Setting mode
    mode = '3'
    s.send(mode.encode())

    # Choosing a file
    sendFileName = input("File name:")
    s.send(str(sendFileName).encode())

    f = open(sendFileName, 'wb')
    print("File opened!")
    while True:
        m = s.recv(2048)
        decodedString = base64.b64decode(m)
        f.write(decodedString)
        print("File is downloading...")
        if not m:
            print("File has been download!")
            break

    f.close()


def upload_to_server():
    # Setting mode
    mode = '2'
    s.send(mode.encode())

    print('Files to upload from:')
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    print(files)
    sendFileName = input("File name:")
    s.send(str(sendFileName).encode())

    file = open(sendFileName, 'rb')
    image_data = file.read(2048)

    while image_data:
        s.send(image_data)
        image_data = file.read(2048)

    print('File upload complete.')
    file.close()


def file_list():
    menu_list = ['1 Local files', '2 Files on server']
    while True:
        for i in menu_list:
            print(i)
        user_choice = input('Choose a number: ')
        if user_choice == '1':
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            print(files)
            break
        elif user_choice == '2':
            mode = '1'
            s.send(mode.encode())
            print("Files on server: " + s.recv(1024).decode())
            break
        else:
            print('That was not a valid number. Please enter your choice again.')


def start_chat():
    print('placeholder')


def login_function():
    username = input('Username: ')
    password = input('Password: ')
    cred = username + "," + password
    s.send(cred.encode())    
    # s.send(password.encode())
    credential_status = s.recv(1024).decode()
    print(credential_status)
    if credential_status == 'Credentials Accepted':
        return
    else:
        login_function()


def menu():
    login_function()
    menu_list = ['1. View files', '2. Download', '3. Upload', '4. Chat', '5. Logout']
    while True:
        for i in menu_list:
            print(i)
        user_choice = input('Choose a number: ')
        # s.send(user_choice.encode())
        if user_choice == '1':
            file_list()
        elif user_choice == '2':
            download_from_server()
            break
        elif user_choice == '3':
            upload_to_server()
            break
        elif user_choice == '4':
            start_chat()
            break
        elif user_choice == '5':
            login_function()
            print('Have a nice day!')
            break
        else:
            print('That was not a valid number. Please enter your choice again.')


# Establishing connection with server.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

menu()
s.close()
