#!/usr/bin/env pythedern
import socket
import paramiko
import sys
import os
import time
import csv

def readCSV(filename):
	s=[]
	firstline = True
        data = csv.reader(open(filename, 'rb'), delimiter=",")
        for row in data:
	    if firstline:    #skip first line
                firstline = False
                continue

            s.append(row)
        return s


def for_suse():
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	send_init("scp -P "+own_port+" root@"+own_ip+":/root/agents/zabbix_suse_64bit.tar.gz /\n",1,True)
	send_init(own_password +"\n",1,True)
	send_init("cd /\n",1,True)
      	send_init("tar -xzvf zabbix_suse_64bit.tar.gz\n",2,True)
	send_init("ls -l /etc/init.d/zabbix_agentd\n",1,True)
      	send_init("chkconfig zabbix_agentd\n",1,True)
	send_init("groupadd zabbix\n",1,True)
	send_init("useradd -g zabbix zabbix\n",1,True)
	send_init("usermod -G sapsys zabbix\n",1,True)
	send_init("sed -i 's/Server=127.0.0.1/Server="+proxy+"/g' /opt/zabbix/etc/zabbix_agentd.conf\n",1,True)
	send_init("sed -i 's/ServerActive=127.0.0.1/ServerActive="+proxy+"/g' /opt/zabbix/etc/zabbix_agentd.conf\n",1,True)
	send_init("sed -i 's|Hostname=Zabbix server|Hostname="+hostname+"|g' /opt/zabbix/etc/zabbix_agentd.conf\n",1,True)
	send_init("chkconfig --level 3,5 zabbix_agentd on\n",1,True)
	send_init("scp -P "+own_port+" root@"+own_ip+":/root/agents/checkro.sh /opt/zabbix\n",1,True)
        send_init(own_password +"\n",1,True)
	send_init("chmod 755 /opt/zabbix/checkro.sh\n",1,True)
	send_init("echo UserParameter=checkro,/opt/zabbix/checkro.sh >> /opt/zabbix/etc/zabbix_agentd.conf\n",1,True)
	send_init("/etc/init.d/zabbix_agentd restart\n",1,True)
	send_init("ps -ef | grep zabbix\n",1,True)
		
def for_ubuntu():
	send_init("scp -P "+own_port+" root@"+own_ip+":/root/agents/zabbix_ubuntutrusty_64bit.rpm /\n",10,True)
	send_init("yes\n",3,True)
	send_init(own_password + "\n",3,True)
	send_init("sudo apt-get update\n",180,True)
	send_init("sudo dpkg -i /zabbix_ubuntutrusty_64bit.rpm\n",10,True)
	send_init("sudo apt-get update\n",60,True)
	send_init("sudo apt-get install zabbix-agent\n",2,True)
        send_init("/etc/init.d/zabbix-agent restart\n",1,True)
		
def for_centos(x):
	send_init("rpm -ivh /opt/zabbix_"+x+"_64bit.rpm\n",1,True)
        send_init("sed -i 's/Server=127.0.0.1/Server="+proxy+"/g' /etc/zabbix/zabbix_agentd.conf\n",1,True)
        send_init("sed -i 's/ServerActive=127.0.0.1/ServerActive="+proxy+"/g' /etc/zabbix/zabbix_agentd.conf\n",1,True)
        send_init("sed -i 's|Hostname=Zabbix server|Hostname="+hostname+"|g' /etc/zabbix/zabbix_agentd.conf\n",1,True)
	send_init("scp -P "+own_port+" root@"+own_ip+":/root/agents/checkro.sh /etc/zabbix\n",1,True)
	send_init(own_password +"\n",1,True)
        send_init("chmod 755 /etc/zabbix/checkro.sh\n",1,True)
	send_init("echo UserParameter=checkro,/etc/zabbix/checkro.sh >> /etc/zabbix/zabbix_agentd.conf\n",1,True)
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
	if any("CentOS" in s for s in c) and any("7" in s for s in c):
		version= 'centos7'
		f.write(version+",")
		shell.send("arch\n")
                time.sleep(wait_time)
                bits= shell.recv(1024).split("\n")
                if any("64" in s for s in bits):
                        send_init("scp -P "+own_port+" root@"+own_ip+":/root/agents/zabbix_"+version+"_64bit.rpm /opt/\n",1,True)
                        send_init("yes\n",3,True)
                        send_init(own_password + "\n",1,True)
                else:
                        send_init("scp -P "+own_port+" root@"+own_ip+":/root/agents/zabbix_"+version+"_32bit.rpm /opt/\n",1,True)
                        send_init("yes\n",3,True)
                        send_init(own_password + "\n",1,True)

		for_centos(version)

	elif any("CentOS" in s for s in c)and any("6" in s for s in c):
		version= 'centos6'
		f.write(version+",")
		shell.send("arch\n")
		time.sleep(wait_time)
		bits= shell.recv(1024).split("\n")
		if any("64" in s for s in bits):
                	send_init("scp -P "+own_port+" root@"+own_ip+":/root/agents/zabbix_"+version+"_64bit.rpm /opt/\n",1,True)
			send_init("yes\n",3,True)
                	send_init(own_password + "\n",1,True)
		else:
			send_init("scp -P "+own_port+" root@"+own_ip+":/root/agents/zabbix_"+version+"_32bit.rpm /opt/\n",1,True)
                        send_init("yes\n",3,True)
                        send_init(own_password + "\n",1,True)
               
		for_centos(version)
		#shell.send("arch\n")

	elif any("CentOS" in s for s in c) and any("5" in s for s in c):
                version= 'centos5'
		f.write(version+",")
		shell.send("arch\n")
                time.sleep(wait_time)
                bits= shell.recv(1024).split("\n")
                if any("64" in s for s in bits):
                        send_init("scp -P "+own_port+" root@"+own_ip+":/root/agents/zabbix_"+version+"_64bit.rpm /opt/\n",1,True)
                        send_init("yes\n",3,True)
                        send_init(own_password + "\n",1,True)
                else:
                        send_init("scp -P "+own_port+" root@"+own_ip+":/root/agents/zabbix_"+version+"_32bit.rpm /opt/\n",1,True)
                        send_init("yes\n",3,True)
                        send_init(own_password + "\n",1,True)
                for_centos(version)

	elif any("ubuntu" in s for s in c):
		f.write("ubuntu,")
		for_ubuntu()
	else:
		f.write("suse,")
		for_suse()
	
with open ("result.csv","wb+") as f:
	f.write("Operating system, Ip, Username, Pasword, Port, Status\n")
	data= readCSV("serverback.csv")
	for d in data:
		if str(d[0]) !="nan":
			system_ip = str(d[0])
			system_username = str(d[1])
			system_ssh_password = str(d[2])
			por = int(d[3])
			proxy = str(d[4])
			hostname = str(d[5])
			own_password = str(d[7])
			client = paramiko.SSHClient()
			own_ip = str(d[6])
			own_port = str(int(d[8]))
		# Make sure that we add the remote server's SSH key automatically
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			print "ip : " , system_ip
		# Connect to the client
 			try:
				client.connect(system_ip,port=por,username=system_username, password=system_ssh_password)
				print "Connected ",client
				# Create a raw shell

				shell = client.invoke_shell()

		# Send the su command
				send_init("sudo su -\n", 1 , True)
		
		# Send the client's su password followed by a newline
				send_init(system_ssh_password + "\n", 1, True)
				send_string_and_wait("cat /etc/*-release\n",1,True)
			

		# Close the SSH connection
                	
				client.close()
			except (paramiko.SSHException, socket.error):
                #the essage will be printed if the connection attempt fails.
                        	print'invalid login password'
				
			if os.system("zabbix_get -s"+system_ip+" -k agent.ping")=="1":
				f.write(system_ip+","+str(por)+","+system_username+","+system_ssh_password+",agent installed successfully\n")
			else:
				f.write(system_ip+","+str(por)+","+system_username+","+system_ssh_password+",error\n")
			
