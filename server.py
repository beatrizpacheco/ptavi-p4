#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

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
                    print("El cliente nos manda:", line.decode('utf-8'))
        print(self.dic)

if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler) #'' es localhost

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever() #Esperando alguna conexion infinitamente
    except KeyboardInterrupt:
        print("Finalizado servidor")
