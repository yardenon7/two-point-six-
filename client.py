"""
author: Yarden Hadas
Date: 19/11
Description: The client. Can ask the server for the time, a random number between
1 and 10, the name of the server and stop the connection with it
"""
import socket
import logging

logging.basicConfig(filename="log_client.log", level="DEBUG")
MAX_PACKET = 1024
IP = '127.0.0.1'
PORT = 1729
INVALID_COMMAND = "invalid command"


def checking_the_request(request):
    """
    :param request: the request the client want to ask the server
    :return: true of the request is valid and false otherwise
    """
    return request == 'TIME' or request == 'NAME' or request == 'RAND' or request == 'EXIT'


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((IP, PORT))
        response = ""
        while response != "bye":
            request = input("enter the request: ")
            logging.debug("the request was: " + request)
            if checking_the_request(request):
                my_socket.send(request.encode())
                response = my_socket.recv(MAX_PACKET).decode()
                logging.debug("the response was: " + response)
                print(response)
            else:
                logging.debug("The request: " + request + " didn't return any data info")
                print(INVALID_COMMAND)
    except socket.error as err:
        print('received socket error ' + str(err))
    finally:
        my_socket.close()


if __name__ == '__main__':
    """
    checking
    """
    assert checking_the_request("TIME")
    assert checking_the_request("EXIT")
    assert checking_the_request("RAND")
    assert checking_the_request("NAME")
    assert not checking_the_request("")
    assert not checking_the_request("name")
    assert not checking_the_request("rfg")
    assert not checking_the_request("rfg12345**??")

    main()
