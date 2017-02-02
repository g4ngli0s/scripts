#!/usr/bin/python
#
# Decodifica una cadena HEX a ASCII
# 
# by sn4fu (20170202)
#
print "\nDecodificador de HEX a ASCII (by sn4fu)\n"
cadena = raw_input("Introduzca la cadena a decodificar: ")
cadena_ascii = cadena.decode("hex")
print '\nCadena en ASCII:\n'+cadena_ascii
