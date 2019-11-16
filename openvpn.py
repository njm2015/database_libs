import os
import pandas as pd
import random
import re
import signal
import subprocess
import sys
import time

from boolean_execution_pipeline import BooleanExecutionPipeline
from flask import Flask
from telnetlib import Telnet

vpn_cmd = 'openvpn --config /etc/openvpn/ovpn_tcp/{} --auth-user-pass ~/.auth.txt &'
server_filename_prefix = '/etc/openvpn/ovpn_tcp/'
get_pid_str = 'ps aux | grep openvpn'
kill_pid = 'sudo kill -9 {}'

config_management_str = 'management localhost 7505\n'

state_str = b'state\n'
kill_str = b'signal SIGTERM\n'

server_f = open('./servers.txt')
server_list = list(server_f)


def handler(signum, frame):
	print('Exiting cleanly...')
	server_f.close()
	kill_openvpn()
	sys.exit(0)


def modify_config_files():

	with open('./servers.txt', 'r') as f:
		for line in f.readlines():
			with open(server_filename_prefix + line.strip(), 'r') as config:
				flag = (config.readlines()[-1].strip() == config_management_str.strip())
			if not flag:
				with open(server_filename_prefix + line.strip(), 'a+') as config_write:
					config_write.write(config_management_str)


def start_openvpn():

	subprocess.run(vpn_cmd.format(random.choice(server_list).strip()), shell=True)
	return True

def restart_openvpn():
	return restart_pipeline.execute()


def openvpn_status():
	try:
		with Telnet('localhost', 7505) as tn:
			for i in range(200):
				try:
					tn.write(state_str)
					success_str = tn.read_until(b'SUCCESS', 0.1).decode('ascii')
					print('success_str')
					print(success_str)
					if 'SUCCESS' in success_str:
						return True

				except EOFError:
					return restart_openvpn()

		return restart_openvpn()
	except ConnectionRefusedError:
		print('openvpn.py: 64')
		return False


def kill_openvpn():

	try:
		with Telnet('localhost', 7505) as tn:
			tn.write(kill_str)
			success_str = tn.read_all().decode('ascii')

		print(success_str)
		return 'SUCCESS' in success_str
	except:
		pass

restart_pipeline = BooleanExecutionPipeline([
	kill_openvpn,
	start_openvpn,
	openvpn_status
], sleep_time=2)


change_server_pipeline = BooleanExecutionPipeline([
	openvpn_status,
	kill_openvpn,
	start_openvpn,
	openvpn_status
],[
	start_openvpn,
	openvpn_status
], sleep_time=2)


def change_server():
	return change_server_pipeline.execute()


if __name__ == '__main__':
	# change_server()
	kill_openvpn()
	