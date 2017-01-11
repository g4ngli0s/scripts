#!/bin/bash 
#
# base64_recursive_decoder
#
# Rev.20170111
# by sn4fu 
#

exec 2>/dev/null

if [[ $# -eq 0 ]] ; then
   echo 'Decodifica recursivamente un fichero de texto msg.txt en base64, buscando una cadena de texto.'
   echo 'Uso: ./base64_recursive_decoder <iteraciones> <cadena>'
   exit 0
fi

cp msg.txt 1.txt

for ((i=1; i<=$(($1 - 1)); i++)); do
   cat $i.txt | base64 -d > $(($i + 1)).txt
   if grep -r $2 $(($i + 1)).txt; then
      printf "\nCadena encontrada en la Iteracion $i\n"
      rm $i.txt $(($i + 1)).txt
      exit 0
   else 
      rm $i.txt
      a=$((i+1))
   fi
done

rm $a.txt
