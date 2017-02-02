#!/usr/bin/python
#
# Decodifica una cadena de Base64 a ASCII
# 
# by sn4fu (20170202)
#
import base64
print "\nDecodificador de Base64 a ASCII (by sn4fu)\n"
cadena = raw_input("Introduzca la cadena a decodificar: ")
cadena = cadena.replace("\n","")
cadena_ascii = base64.b64decode(cadena) 
print '\nCadena en ASCII:\n'+cadena_ascii
