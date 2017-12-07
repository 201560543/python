import os
#centos
os.system("wget -O agents/zabbix_centos5_32bit.rpm https://repo.zabbix.com/zabbix/3.0/rhel/5/i386/zabbix-agent-3.0.4-1.el5.i386.rpm")
os.system("wget -O agents/zabbix_centos5_64bit.rpm https://repo.zabbix.com/zabbix/3.0/rhel/5/x86_64/zabbix-agent-3.0.4-1.el5.x86_64.rpm")
os.system("wget -O agents/zabbix_centos6_32bit.rpm https://repo.zabbix.com/zabbix/3.0/rhel/6/i386/zabbix-agent-3.0.4-1.el6.i686.rpm")
os.system("wget -O agents/zabbix_centos6_64bit.rpm https://repo.zabbix.com/zabbix/3.0/rhel/6/x86_64/zabbix-agent-3.0.4-1.el6.x86_64.rpm")
os.system("wget -O agents/zabbix_centos7_64bit.rpm https://repo.zabbix.com/zabbix/3.0/rhel/7/x86_64/zabbix-agent-3.0.4-1.el7.x86_64.rpm")
#ubuntu
#os.system("wget -O agents/zabbix_ubuntutrusty_32bit.rpm https://repo.zabbix.com/zabbix/3.0/ubuntu/pool/main/z/zabbix/zabbix-agent_3.0.4-1+trusty_i386.deb")
#os.system("wget -O agents/zabbix_ubuntutrusty_64bit.rpm https://repo.zabbix.com/zabbix/3.0/ubuntu/pool/main/z/zabbix/zabbix-agent_3.0.4-1+trusty_amd64.deb")
os.system("wget -O agents/zabbix_ubuntutrusty_64bit.rpm http://repo.zabbix.com/zabbix/3.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_3.0-2+xenial_all.deb")
#suse
os.system("wget -O agent/checkro.sh ftp://192.168.255.132/checkro.sh")
os.system("wget -O agents/zabbix_suse_64bit.tar.gz ftp://192.168.255.132/zabbix_agent_suse11_sp3_64bit.tar.gz")
