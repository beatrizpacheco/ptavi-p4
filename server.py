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

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.wfile.write(b"Hemos recibido tu peticion") #La b pasa a bytes
        for line in self.rfile:
            print(self.client_address)
            print("El cliente nos manda: ", line.decode('utf-8'))

if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', PORT), EchoHandler) #'' es localhost

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever() #Esperando alguna conexion infinitamente
    except KeyboardInterrupt:
        print("Finalizado servidor")
