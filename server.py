#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import json
import socketserver
import sys
import time
from time import gmtime , strftime

if len(sys.argv) < 2:
    sys.exit("Usage: python3 server.py puerto")

PORT = int(sys.argv[1])

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dic = {}
    
    def json2registered(self):
        with open('registered.json', 'r') as fich:
            for linea in fich:
                print('holaaaaaa' +linea)
                self.dic = json.loads(linea)
                print('estoy en json2...' + str(self.dic))
                #Lo coge bien del fichero, pero los demas def no lo usan bien
    
    def register2json(self):
        json.dump(self.dic, open('registered.json', "w"))
    
    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        print('estoy en handle' + str(self.dic))
        for line in self.rfile:
            message = line.decode('utf-8').split()
            if message:
                if message[0] == 'REGISTER':
                    user = message[1][4:]
                    info = self.client_address[0]
                if message[0] == 'Expires:':
                    if message[1] != '0':
                        Expire = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()+int(message[1])))
                        self.dic[user] = [info, Expire]
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    elif message[1] == '0':
                        try:
                            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                            del self.dic[user]
                        except KeyError:
                            self.wfile.write(b"SIP/2.0 404 User Not Found\r\n\r\n")
            print(line.decode('utf-8'), end='')
        print(self.dic)
        self.register2json()


if __name__ == "__main__":
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler) #'' es localhost
    SIPRegisterHandler.json2registered(serv)
    print('estoy en el main' + str(serv.dic))
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever() #Esperando alguna conexion infinitamente
    except KeyboardInterrupt:
        print("Finalizado servidor")
