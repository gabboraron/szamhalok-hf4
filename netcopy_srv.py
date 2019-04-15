import socket
import struct
import sys
import os
import zlib

#TCP server communication
server_ip 	= sys.argv[1]
server_port = int(sys.argv[2])

sock 			= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address 	= (server_ip, server_port)
sock.bind(server_address)

#Checksum server communication
check_server_ip 	= sys.argv[3]
check_server_port 	= int(sys.argv[4])

#File access part
file_id 	= sys.argv[5]
file_path 	= sys.argv[6]

sock.listen(1)
eof = False
while (not eof):
	connection, client_address = sock.accept()
	data = connection.recv(1024)
	#print("Connenction detected")
	data = data.decode('UTF-8')
	text = ""
	while data != "EOF":
		text = text + data
		data = connection.recv(1024)
		data = data.decode('UTF-8')
		#print("data: " + data)
	eof = True
	with open(file_path, 'w') as f:
		f.write(text)
	f.close()
	#print("File saved")
#data = connection.recv(1024)
#print(data.decode('UTF-8'))
connection.close()

#Checksum part
#get checksum
crc = hex(zlib.crc32((text).encode('UTF-8')) % (1<<32) )
#print("CRC: " + str(crc))
#connect to checksum server
connection_crc 		= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
check_server_address 	= (check_server_ip, check_server_port)
connection_crc.connect(check_server_address)
crc_length = len(crc)
crc_data = "KI|"+file_id
connection_crc.sendall(crc_data.encode('UTF-8'))
checksum = connection_crc.recv(crc_length)
connection_crc.close()

checksum = checksum.decode('UTF-8')
checksum = str(checksum)
#print("given CRC: " + checksum)

if (checksum == crc):
	print("CSUM OK")
else:
	print("CSUM CORRUPTED")