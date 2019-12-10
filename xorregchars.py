#!/usr/bin/python
#
# Dados unos codigos de caracteres validos, halla las combinaciones de esos bytes tomados de 4 en 4.
# Para luego hacer el AND entre cada uno de los valores para encontrar los que dan 0
# Usado para codificar shellcodes cuando necesitas poner a 0 un registro
# Ej: AND EAX,50503235 AND EAX,25254D4A
# by ring3rbell (20191210)
#
import pdb
import itertools


if __name__=='__main__':

	#pdb.set_trace()
	goodvalues = "\x25\x2a\x2d\x31\x32\x35\x4a\x4d\x4e\x50\x55\x5c"
	#goodvalues = "\x10\x25\xef\xda"

	# Preguntamos cuantos valores queremos que nos muestre:
	pregunta = raw_input("Cuantos valores desea mostrar: ")
	valores = int(pregunta)
	
	#Pasamos los valores de los chars a hexadecimal y le quitamos el 0x
	toencode = []
	for c in goodvalues:
		toencode.append(hex(ord(c)).lstrip('0x'))

	# Hallamos las permutaciones con repeticion de cada char tomados de 4 en 4
	combinaciones = [p for p in itertools.product(toencode, repeat=4)]

	# Convertimos los valores a hexadecimal
	todoval = []
	for c in combinaciones:
		todoval.append(hex(int(''.join(c),16)))

	# Buscamos los que dan val1 AND val2 = 0x0
	cuenta = 0
	for i in range(0,len(todoval)):
		val1 = int(todoval[i],16)
		if cuenta >= valores:
			print cuenta,valores				
			break
		for j in range(0,len(todoval)):
			val2 = int(todoval[j],16)
			if val1 & val2 == 0:
				print todoval[i] + ' AND ' + todoval[j] + ' = 0x0'
				cuenta += 1
				if cuenta >= valores:
					print cuenta,valores				
					break
				
