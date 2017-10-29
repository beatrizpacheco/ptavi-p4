#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import json
import socketserver
import sys
import time
from time import gmtime, strftime

if len(sys.argv) < 2:
    sys.exit("Usage: python3 server.py puerto")
PORT = int(sys.argv[1])


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dic = {}

    def json2registered(self):
        try:
            with open('registered.json', 'r') as fich:
                self.dic = json.load(fich)
        except:
            pass

    def register2json(self):
        json.dump(self.dic, open('registered.json', "w"))

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.json2registered()
        for line in self.rfile:
            message = line.decode('utf-8').split()
            if message:
                if message[0] == 'REGISTER':
                    user = message[1][4:]
                    info = self.client_address[0]
                if message[0] == 'Expires:':
                    if message[1] != '0':
                        Expire = time.strftime('%Y-%m-%d %H:%M:%S',
                                               time.gmtime(time.time() +
                                                           int(message[1])))
                        self.dic[user] = [info, Expire]
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    elif message[1] == '0':
                        try:
                            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                            del self.dic[user]
                        except KeyError:
                            self.wfile.write(b'SIP/2.0 404 User'
                                             b'Not Found\r\n\r\n')
            print(line.decode('utf-8'), end='')
        print(self.dic)
        self.register2json()


if __name__ == "__main__":
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()  # Esperando alguna conexion infinitamente
    except KeyboardInterrupt:
        print("Finalizado servidor")
