"""
author: Yarden Hadas
Date: 19/11
Description: The server. Will return the time, random number between 1 and 10 and
the name of the server, depending on what the client asked. Could also end and start a new connection with another
client
"""
import socket
import datetime
import random
import logging

logging.basicConfig(filename="log_server.log", level="DEBUG")
QUEUE_LEN = 1
MAX_PACKET = 4
IP = '0.0.0.0'
PORT = 1729
LAST_MASSAGE = "bye"
NAME_OF_SERVER = "the greatest server"


def send_request(request, client_socket):
    """

    :param request: the request that was sent by the client
    :param client_socket: the socket that connect the client and the server
    :return: none
    """
    if request == "TIME":
        tm = str(datetime.datetime.now())
        logging.debug("the response is: " + tm)
        client_socket.send(tm.encode())
    elif request == "NAME":
        logging.debug("the response is: " + ask_for_name())
        client_socket.send(ask_for_name().encode())
    elif request == "RAND":
        randi = str(ask_for_random())
        logging.debug("the response is: " + randi)
        client_socket.send(randi.encode())
    elif request == "EXIT":
        logging.debug("the response is: " + ask_for_exit())
        client_socket.send(ask_for_exit().encode())


def ask_for_name():
    """
    :return: the name of the server
    """
    return NAME_OF_SERVER


def ask_for_random():
    """
    :return: A random number between 1 and 10
    """
    return random.randint(1, 10)


def ask_for_exit():
    """
    :return: the massage 'bye'"
    """
    return LAST_MASSAGE


def main():
    socketi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socketi.bind((IP, PORT))
        logging.debug("the socket connected successfully")
        socketi.listen(QUEUE_LEN)
        while True:
            client_socket, client_address = socketi.accept()
            try:
                request = client_socket.recv(MAX_PACKET).decode()
                logging.debug("the request was: " + request)
                while request != "EXIT":
                    send_request(request, client_socket)
                    request = client_socket.recv(MAX_PACKET).decode()
                    logging.debug("the request was: " + request)
            except socket.error as err:
                print('received socket error on client socket' + str(err))
            finally:
                msg = LAST_MASSAGE
                client_socket.send(msg.encode())
                client_socket.close()
                logging.debug("the server has done connecting with the client")
    except socket.error as err:
        print('received socket error on server socket' + str(err))
    finally:
        socketi.close()


# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    """
     checking
     """
    assert ask_for_name() == "the greatest server"
    assert ask_for_random() <= 10
    assert ask_for_random() >= 1
    assert ask_for_exit() == "bye"
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
