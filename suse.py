#!/usr/bin/env python
import socket
import paramiko
import sys
import os
import time
import pandas as pd

#os.system('wget http://repo.zabbix.com/zabbix/3.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_3.0-2+xenial_all.deb')
#os.system('wget ftp://192.168.255.132/zabbix-agent-3.0.11-1.el7.x86_64.rpm')

def readCSV(filename):
	data = pd.read_csv(filename)
	return data.values

def for_suse():
	send_init("scp -r root@192.168.255.166:/root/agents/zabbix_suse_64bit.tar.gz /\n",1,True)
	send_init(own_password +"\n",1,True)
	send_init("cd /\n",1,True)
      	send_init("tar -xzvf zabbix_suse_64bit.tar.gz\n",2,True)
	send_init("ls -l /etc/init.d/zabbix_agentd\n",1,True)
      	send_init("chkconfig zabbix_agentd\n",1,True)
	send_init("groupadd zabbix\n",1,True)
	send_init("useradd -g zabbix zabbix\n",1,True)
	send_init("usermod -G sapsys zabbix\n",1,True)
	send_init("sed -i 's/Server=127.0.0.1/Server=192.168.255.132/g' /opt/zabbix/etc/zabbix_agentd.conf\n",1,True)
	send_init("sed -i 's/ServerActive=127.0.0.1/ServerActive=192.168.255.132/g' /opt/zabbix/etc/zabbix_agentd.conf\n",1,True)
	send_init("sed -i 's|Hostname=Zabbix server|Hostname=cloud|g' /opt/zabbix/etc/zabbix_agentd.conf\n",1,True)
	send_init("chkconfig --level 3,5 zabbix_agentd on\n",1,True)
	send_init("scp -r root@192.168.255.166:/root/agents/checkro.sh /opt/zabbix\n",1,True)
        send_init(own_password +"\n",1,True)
	send_init("chmod 755 /opt/zabbix/checkro.sh\n",1,True)
	send_init("echo UserParameter=checkro,/opt/zabbix/checkro.sh >> /opt/zabbix/etc/zabbix_agentd.conf\n",1,True)
	send_init("/etc/init.d/zabbix_agentd restart\n",1,True)
	send_init("ps -ef | grep zabbix\n",1,True)
		
def for_ubuntu():
	send_init("scp -r root@192.168.255.166:/root/agents/zabbix_ubuntutrusty_64bit.rpm /\n",1,True)
	#send_init("yes\n",1,True)
	send_init(own_password + "\n",1,True)
	send_init("sudo apt-get update\n",60,True)
	send_init("sudo dpkg -i /zabbix_ubuntutrusty_64bit.rpm\n",5,True)
	send_init("sudo apt-get update\n",5,True)
	#send_init("sudo apt-get install zabbix-agent\n",2,True)
        #send_init("/etc/init.d/zabbix-agent restart\n",1,True)
		
def for_centos():
	send_init("scp -r root@192.168.255.166:/root/agents/  /opt/\n",1,True)
        send_init(own_password + "\n",1,True)
	send_init("rpm -ivh /opt/zabbix-agent-3.0.4-1.el7.x86_64.rpm\n",1,True)
        send-init("sed -i 's/Server=127.0.0.1/Server=192.168.255.132/g' /etc/zabbix/zabbix_agentd.conf\n",1,True)
        send_init("sed -i 's/ServerActive=127.0.0.1/ServerActive=192.168.255.132/g' /etc/zabbix/zabbix_agentd.conf\n",1,True)
        #shell.send("sed -i 's/Hostname=\(*\)/Hostname=cloudwebserver/g' /etc/zabbix/zabbix_agentd.conf\n")
        send_init("service zabbix-agent start\n",1,True)
        send_init("service zabbix-agent enable\n",1,True)
        send_init("service zabbix-agent status\n",1,True)	

def send_init(command,wait_time,should_print):
    shell.send(command)
    # Wait a bit, if necessary
    time.sleep(wait_time)
    # Flush the receive buffer
    receive_buffer = shell.recv(1024)
    # Print the receive buffer, if necessary
    if should_print:
	print receive_buffer

def send_string_and_wait(command,wait_time,should_print):
    # Send the su command
    shell.send(command)

    # Wait a bit, if necessary
    time.sleep(wait_time)

    # Flush the receive buffer
    receive_buffer = shell.recv(1024)

    # Print the receive buffer, if necessary
    if should_print:
        c=receive_buffer.split("\n")
	if any("CentOS" and "7" in s for s in c):
		send_init("scp -r root@192.168.255.166:/root/agents/zabbix_centos7_64bit.rpm /opt/\n",1,True)
        	send_init(own_password + "\n",1,True)
		for_centos()

		shell.send("arch\n")

	elif any("ubuntu" in s for s in c):
		#shell.send("arch\n")
		#time.sleep(1)
		#bit=shell.recv(1024)
		#print bit
		for_ubuntu()
	else:
		for_suse()
	
	
data= readCSV("ub.csv")
for d in data:
	if str(d[0]) !="nan":
		system_ip = str(d[0])
		system_username = str(d[1])
		system_ssh_password = str(d[2])
		por = int(d[3])
		own_password = 'Zabbix@123'
		client = paramiko.SSHClient()

		# Make sure that we add the remote server's SSH key automatically
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		print "ip : " , system_ip
		# Connect to the client
		try:
			client.connect(system_ip,port=por,username=system_username, password=system_ssh_password)
			print "Connected ",client
				# Create a raw shell

			#ftp_client=client.open_sftp()
			#ftp_client.put('/root/zabbix-agent-3.0.4-1.el7.x86_64.rpm','/opt/zabbix-agent-3.0.4-1.el7.x86_64.rpm')
			#ftp_client.put('/root/zabbix-release_3.0-2+xenial_all.deb','/opt/zabbix-release_3.0-2+xenial_all.deb')
			#ftp_client.close()
			shell = client.invoke_shell()
			

			#send_string_and_wait("rpm -ivh /opt/zabbix-agent-3.0.4-1.el7.x86_64.rpm\n", 1 , True)
			#send_string_and_wait("sed -i 's/Server=127.0.0.1/Server=192.168.255.132/g' /etc/zabbix/zabbix_agentd.conf\n", 1 , True)
			#send_string_and_wait("sed -i 's/ServerActive=127.0.0.1/ServerActive=192.168.255.132/g' /etc/zabbix/zabbix_agentd.conf\n", 1 , True)
			#send_string_and_wait("sed -i 's/Hostname=\(*\)/Hostname=cloudwebserver/g' /etc/zabbix/zabbix_agentd.conf\n", 1 , True)

			#send_string_and_wait("systemctl start zabbix-agent\n", 1 , True)
			#send_string_and_wait("systemctl enable zabbix-agent\n", 1 , True)
			#send_string_and_wait("systemctl status zabbix-agent\n", 1 , True)

			

		# Send the su command
			send_init("sudo su -\n", 1 , True)
		
		# Send the client's su password followed by a newline
			send_init(system_ssh_password + "\n", 1, True)
			#send_string_and_wait("scp -r root@192.168.255.166:/root/zabbix-release_3.0-2+xenial_all.deb /opt/\n",1,True)
			#send_string_and_wait(own_password + "\n", 1, True)
			send_string_and_wait("cat /etc/*-release\n",1,True)
			
		# Send the install command followed by a newline and wait for the done string
			#send_string_and_wait_for_string(root_command, root_command_result)

		# Close the SSH connection
                	
			client.close()
		#send_string_and_wait("passwd -u ctrls99\n", 1, True)
		except (paramiko.SSHException, socket.error):
                #the essage will be printed if the connection attempt fails.
                        print'invalid login password'
				
		with open ("result.csv","wb") as f:
			if os.system("zabbix_get -s"+system_ip+" -k agent.ping")=="1":
				f.write(system_ip+","+str(por)+","+system_username+","+system_ssh_password+",agent installed successfully\n")
			else:
				f.write(system_ip+","+str(por)+","+system_username+","+system_ssh_password+",error\n")
			
		
