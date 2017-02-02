#!/bin/bash
#
# Aplica el comando strings a los ficheros de todo el arbol
# del directorio que se pasa como parametro.
#
# Uso: strings_recursivo.sh <directorio>
#
# Resultados en 'strings.txt'.
#
# Rev.20170202 by sn4fu
#

arbol=$(mktemp tempfile.XXXXXXXX)
find $1 -type f > $arbol

while read -r line
do
    fichero="$line"
    strings -f $fichero >> strings.txt
done < $arbol

rm $arbol
