#!/usr/bin/perl
#
# bsidessf17 - dnscap
#
# script de volcado de datos de paquetes
#
# fusion_ordenado.txt tiene el formato: <paquete>\t<datos>
#
# Rev.20170212 by sn4fu

use strict;
use warnings;
use 5.016;

my $fichero = 'fusion_ordenado.txt';
open(my $fh,$fichero)
or die "No se ha encontrado el fichero '$fichero' $!";

while (my $linea = <$fh>) {
 chomp $linea;						# quitar CR
 my ($paquete, $datos) = split /\t/, $linea;		# parsear usando TAB como separador
 my @cadenas = split /\./, $datos;			# parsear las partes de la cadena de datos separadas con '.'
 my $cadena_sobrante1 = 'org';				# las cadenas 'org' no nos interesan
 @cadenas = grep {!/$cadena_sobrante1/} @cadenas;
 my $cadena_sobrante2 = 'skullseclabs';
 @cadenas = grep {!/$cadena_sobrante2/} @cadenas;	# las cadenas 'skullseclabs' no no sinteresan
 foreach (@cadenas)
   {
      print "$_\n";					# imprimir los contenidos HEX de interés
   }
}
