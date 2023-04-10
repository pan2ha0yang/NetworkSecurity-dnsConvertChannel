'''
Author       : y0ung
E-mail       : abandonedpeter@outlook.com
Date         : 2023-04-03 22:27:27
LastEditTime : 2023-04-10 12:53:40
FilePath     : \task1\DNSClient.py
Description  : 
Copyright (c) 2023 by WHU-y0ung, All Rights Reserved. 
'''

import socket
import time
import sys

def MakeQueryPack(domain: str):
	TransactionID = 0xffff
	Flags = 0x0000
	Questions = 0x0001
	AnswerRRs = 0x0000
	AuthorityRRs = 0x0000
	AdditionalRRs = 0x0000

	DomainName = b''
	Type = 0x0001
	Class = 0x0001

	TransactionID = TransactionID.to_bytes(2, 'big')
	Flags = Flags.to_bytes(2, 'big')
	Questions = Questions.to_bytes(2, 'big')
	AnswerRRs = AnswerRRs.to_bytes(2, 'big')
	AuthorityRRs = AuthorityRRs.to_bytes(2, 'big')
	AdditionalRRs = AdditionalRRs.to_bytes(2, 'big')

	for s in domain.split('.'):
		DomainName = DomainName + len(s).to_bytes(1, 'big') + s.encode('utf-8')
	DomainName += b'\x00'
	Type = Type.to_bytes(2, 'big')
	Class = Class.to_bytes(2, 'big')

	msg = TransactionID + Flags + Questions + \
		AnswerRRs + AuthorityRRs + AdditionalRRs + \
		DomainName + Type + Class

	return msg


if __name__ == '__main__':
	domain_name = "www.ufw_status = enabled.com"
	domain_name = "www.baidu.com"

	try:
		ip_list = socket.getaddrinfo(domain_name, None)
		print(ip_list)
	except:
		ip_list = []

	if ip_list:
		for i in ip_list:
			print(i[4][0])
		sys.exit()

	server_host = socket.gethostname()
	server_port = 53
	server_addr = (server_host, server_port)

	client_host = ""
	client_port = 9999

	client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# Use bind() To Client's Port, Retry For 3 Times
	retry_cnt = 0
	retry_max = 3
	while True:
		try:
			client_sock.bind((client_host, client_port))
			break
		except Exception as e:
			print("Exception occurred:", e)
			retry_cnt += 1
			if retry_cnt >= retry_max:
				raise e
			else:
				print("Retrying...")
				time.sleep(3)

	try:
		query_pack = MakeQueryPack(domain_name)

		client_sent = client_sock.sendto(query_pack, server_addr)

		server_data, server_addr = client_sock.recvfrom(1024)
		# print(server_data, "\nFrom server IP:", server_addr[0], "port:", server_addr[1])

		# Read Server's Command As ipv4
		cmd = []

		sdata_arr = bytearray(server_data)
		sdata_arr.reverse()
		for i in range(0, len(sdata_arr), 16):
			if bytes(sdata_arr[i+10:i+16]) != b'\x01\x00\x01\x00\x0c\xc0':
				break
			tmp = sdata_arr[i:i+4]
			tmp.reverse()
			cmd.append(tmp)
		
		cmd.reverse()
		for ip in cmd:
			print(str(ip[0]) + "." + str(ip[1]) + "." + str(ip[2]) + "." + str(ip[3]))
		
		# Read Server's Command At The Same Time
		command = bytearray(b'')
		for ip in cmd:
			command = command + ip
		command = command.decode('utf-8')
		print(command)

	finally:
		client_sock.close()