#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import json
import socketserver
import sys

if len(sys.argv) < 2:
    sys.exit("Usage: python3 server.py puerto")

PORT = int(sys.argv[1])

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dic = {}
    
    def register2json(self):
        json.dump(self.dic, open('registered.json', "w"))
    
    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n") #La b pasa a bytes
        for line in self.rfile:
            if line:
                if line.decode('utf-8')[:8] == 'REGISTER':
                    user = line.decode('utf-8')[13:-10]
                    self.dic[user] = self.client_address[0]
                elif line.decode('utf-8')[:7] == 'Expires':
                    if line.decode('utf-8').split(' ')[1][0] == '0':
                        del self.dic[user]
            print(line.decode('utf-8'), end='')
        print(self.dic)
        self.register2json()
    
    


if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler) #'' es localhost

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever() #Esperando alguna conexion infinitamente
    except KeyboardInterrupt:
        print("Finalizado servidor")
