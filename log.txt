import socket
import struct
import sys
import os
import zlib

#TCP server communication
server_ip 	= sys.argv[1]
server_port = int(sys.argv[2])

connection 		= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address 	= (server_ip, server_port)
connection.connect(server_address)

#Checksum server communication
check_server_ip 	= sys.argv[3]
check_server_port 	= int(sys.argv[4])
connection_crc 		= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
crc_server_address 	= (check_server_ip, check_server_port)

#File access part
file_id 	= sys.argv[5]
file_path 	= sys.argv[6]

#Checksum part
#get text
text = ""
with open(file_path, 'r') as ff:
	for line in ff:
		text = text + line
ff.close()
#get checksum
crc = hex(zlib.crc32((text).encode('UTF-8')) % (1<<32) )
#connect to checksum server
connection_crc.connect(crc_server_address)
crc_length = len(crc)
crc_data = "BE|"+str(file_id)+"|60|"+str(crc_length)+"|"+str(crc)
connection_crc.sendall(crc_data.encode('UTF-8'))
connection_crc.close()
#print(crc_data)

#send to TCP server
#text = ""
with open(file_path, 'r') as f:
	#File move part
	for line in f:
		#send file line by line
		connection.sendall(line.encode('UTF-8'))
		#text = text + line
		#print("line: " + line)
	else:
		#Send file end
		eof_msg = "EOF"
		connection.sendall(eof_msg.encode('UTF-8'))

connection.close()
