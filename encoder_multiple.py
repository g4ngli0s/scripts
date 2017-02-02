#!/usr/bin/python
#
# Codifica una cadena ASCII a Base16, Base32, Base64, Hex y Hex-URL
# 
# by sn4fu (20170202)
#
import base64

print "\nCodificador de ASCII a Base16, Base32, Base64, Hex y Hex-URL (by sn4fu)\n"

cadena = raw_input("Introduzca la cadena a codificar: ")
cadena = cadena.replace("\n","")
cadena_base16 = base64.b16encode(cadena)
cadena_base32 = base64.b32encode(cadena)
cadena_base64 = base64.b64encode(cadena)
cadena_hex = cadena.encode("hex")

def insertar_porcentajes(string, every=2):
    lines = []
    for i in xrange(0, len(string), every):
        lines.append(string[i:i+every])
    return '%'.join(lines)
cadena_url = insertar_porcentajes(cadena_hex)
cadena_url = '%' + cadena_url

print '\nCadena en Base16;\n'+cadena_base16
print '\nCadena en Base32:\n'+cadena_base32 
print '\nCadena en Base64:\n'+cadena_base64
print '\nCadena en hexadecimal:\n'+cadena_hex
print '\nCadena en hex-url:\n'+cadena_url
