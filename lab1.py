"""
CPSC 5520, Seattle University
This is the client program lab1.py that sends JOIN message to GCD server on host cs2.seattleu.edu and port 23600.
Then it sends HELLO message to all the groups it received in response from the server.
:Authors: Fnu Shipra
:Version: 0.0
"""
import pickle
import socket
import socketserver
import sys
from socket import error as socket_error

class Lab1(object):

    """
    Constructor to initialize the host and port
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.members = []

    """
    Method that sends pickled message to the server and receives the response and unpickle it.
    Created this method for code reusablility
    """
    def send_message_to_server(self, message, s):
        pickled_message = pickle.dumps(message)
        s.sendall(pickled_message)
        data = s.recv(1024)
        response = pickle.loads(data)
        return response

    """
    Method that makes the connection with GCD server to send and receive the messages by calling
    another method send_message_to_server.
    """
    def join_group(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            message = 'JOIN'
            self.members = self.send_message_to_server(message, s)                  # calling send_message_to_server with JOIN message

            for member in self.members:
                print('HELLO to {}'.format(member))
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    eachHost = member['host']
                    eachPort = member['port']
                    sock.settimeout(1.5)
                    try:
                        sock.connect((eachHost, eachPort))
                    except Exception as err:
                        print('failed to connect: {}', err)
                    else:
                        message = 'HELLO'
                        response = self.send_message_to_server(message, sock)
                        print(response)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python lab1.py HOST PORT")
        exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    obj = Lab1(host, port)                                                      # creating obj object of class Lab1
    obj.join_group()                                                            # calling join_group() method