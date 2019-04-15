import socket
import struct
import sys
import os
import zlib
import select

#DB
crc_db = dict()

#TCP server communication
server_ip 	= sys.argv[1]
server_port = int(sys.argv[2])

sock 			= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address 	= (server_ip, server_port)
sock.bind(server_address)


inputs = [sock]
sock.listen(1)
while True:
	ready_to_read_from, ready_to_write_on,some_exception = select.select(inputs,[],[])
	for s in ready_to_read_from:
		if s is sock:
			connection, client_address = s.accept()
			inputs.append(connection)
			#print('Kapcsolodott valaki')
		else:
			data = s.recv(1024)
			data = data.decode('UTF-8')
			#print("data: " + data)
			direction 	= data.split('|')[0]
			#print("dir: " + direction)

			if direction == "BE":
				file_id		= data.split('|')[1]
				valid_time	= data.split('|')[2]
				crc_length	= data.split('|')[3]
				crc			= data.split('|')[4]
				#print("id:" + file_id)
				#print("time:" + valid_time)
				#print("crc length:" + crc_length)
				#print("crc:" + crc)


				crc_db[file_id] = [crc, valid_time]
				#print("BE: " + str(crc_db[file_id][0]))
			if direction == "KI":
				file_id		= data.split('|')[1]
				#print("id:" + file_id)

				#print("KI: " + str(crc_db[file_id][0]))
				connection.sendall(str(crc_db[file_id][0]).encode('UTF-8'))
				del crc_db[file_id]