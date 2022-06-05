import base64
import os
import socket
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 12000  # The port used by the server
username = ""


def printMenu():
    menu = '__       __                               \n' \
           '/  \     /  |                              \n' \
           '$$  \   /$$ |  ______   _______   __    __ \n' \
           '$$$  \ /$$$ | /      \ /       \ /  |  /  |\n' \
           '$$$$  /$$$$ |/$$$$$$  |$$$$$$$  |$$ |  $$ |\n' \
           '$$ $$ $$/$$ |$$    $$ |$$ |  $$ |$$ |  $$ |\n' \
           '$$ |$$$/ $$ |$$$$$$$$/ $$ |  $$ |$$ \__$$ |\n' \
           '$$ | $/  $$ |$$       |$$ |  $$ |$$    $$/ \n' \
           '$$/      $$/  $$$$$$$/ $$/   $$/  $$$$$$/  \n'
    print(menu)


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
        if m.decode() == 'eof':
            print("File has been download!")
            break
        decodedString = base64.b64decode(m)
        print("File is downloading...")
        f.write(decodedString)

    f.close()


def upload_to_server():
    # Setting mode
    mode = '2'
    s.send(mode.encode())

    # print("Start uploading " + sendFileName)
    print('Files to upload from:')
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    print(files)

    sendFileName = input("File name:")
    # if sendFileName not in files:
    #     print("Invalid FileName")
    #     # s.send("".encode())
    #     return

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


def batch_download():
    t0 = time.time()
    mode = '5'
    s.send(mode.encode())
    files = s.recv(1024).decode()
    sliced = files[2:-2]
    split = sliced.split("', '")
    print(split)

    for i in split:
        print(i)
        s.send(str(i).encode())
        f = open(i, 'wb')
        print("File opened!")
        while True:
            m = s.recv(2048)
            if m.decode() == 'nextfile':
                print("File has been downloaded!")
                break
            decodedString = base64.b64decode(m)
            f.write(decodedString)
            print("File is downloading...")
            print(m)
        f.close()
    t1 = time.time()
    total_time = t1 - t0
    print("All files have been downloaded!")
    print("Total downloading time was", total_time, 'seconds.')


def start_chat():
    # Initially we'll get the entire chat from the server
    mode = '4'
    s.send(mode.encode())
    print('Chat Logs:')
    while True:
        chat = s.recv(1024)
        if chat.decode() == 'eof':
            print('---End of Chat---')
            break
        decodeChat = base64.b64decode(chat)
        print(str(decodeChat, 'UTF-8'))

    # Now we will start an udp connection to carry out the chat functionality
    msg = input(f'[{username}]: ')
    toSend = username + '.!?' + msg
    s.send(toSend.encode())


def login_function():
    global username
    choice = input("Do you want to login ? y/n : ")
    if choice == "n":
        return False
    elif choice != "y":
        print("Only y/n answer accepted")
        return login_function()
    while True:
        username = input('Username: ')
        password = input('Password: ')
        cred = username + "," + password
        s.send(cred.encode())
        credential_status = s.recv(1024).decode()
        print(credential_status)
        if credential_status == 'Credentials Accepted':
            return True
        else:
            choice = ""
            while choice == "":
                choice = input("Do you want to try again? y/n : ")
                if choice == "n":
                    return False
                elif choice == "y":
                    break
                else:
                    choice = ""


def menu():
    if not login_function():
        return
    menu_list = ['1. View files', '2. Download', '3. Upload', '4. Chat', '5. Batch download', '6. Logout']
    while True:
        for i in menu_list:
            print(i)
        user_choice = input('Choose a number: ')
        if user_choice == '1':
            file_list()
        elif user_choice == '2':
            download_from_server()
        elif user_choice == '3':
            upload_to_server()
        elif user_choice == '4':
            start_chat()
        elif user_choice == '5':
            batch_download()
        elif user_choice == '6':
            mode = '6'
            s.send(mode.encode())
            break
        else:
            print('That was not a valid number. Please enter your choice again.')
    menu()


# Establishing a TCP connection with server.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Establishing a UDP connection with the server
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
udp.connect((HOST, 12001))

menu()
s.send("".encode())
print("See you again")
s.close()
