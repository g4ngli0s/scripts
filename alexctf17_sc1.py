#!/usr/bin/python
#
# Script para el reto SC1 de AlexCTF 2017
# 
# by sn4fu (20170204)
#

import socket
import sys

# Crear socket TCP/IP 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('195.154.53.62', 1337)

# Conexion al servidor:
sock.connect(server_address)

while True:
    datos = sock.recv(4096)		              # Recibir datos del servidor
    print datos
    lineas = datos.split('\n')		          # Dividir los datos en un array de lineas
    operacion = lineas[-2]		              # En la penultima linea sale la operacion
    operacion = operacion[:-2]		          # Quitar el ' =' del final
    print operacion 
    resultado = str(eval(operacion)) + "\n"	# Evaluar operacion y convertir a string
    print resultado
    sock.sendall(resultado)		              # Enviar datos al servidor
sock.close()
