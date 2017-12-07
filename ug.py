from pyzabbix import ZabbixAPI

zapi = ZabbixAPI("http://192.168.255.166/zabbix")
zapi.login("Admin", "Ge/\/\$@321")
print("Connected to Zabbix API Version %s" % zapi.api_version())

hostgrps = zapi.hostgroup.get(output=['groupid'])
#print hostgrps

#for h in hostgrps:
	
	#print (h['groupid'].encode('utf-8'))
	#a= zapi.usergroup.massadd(usrgrpids=116,rights= {'permission' : 1, 'id':'h["groupid"]'})
#a= zapi.usergroup.create(name="test-usegrp",rights= {"permission":1,"id":"976"})

a= zapi.usergroup.create(name= 'testusegrp1',
        		 rights= {
            		"permission": 1,
            		"id": "976"
        		},
        		 userids= "121")

print a
