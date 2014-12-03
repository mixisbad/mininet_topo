#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import RemoteController
from time import sleep

class RoundRobinTopo(Topo):
	def __init__(self, servers, total):
		Topo.__init__(self)
		
		#Entry switch
		entrySwitch = self.addSwitch('s%d' %(servers + 1))

		#Initialize servers and switches
		for h in range (1, servers + 1):
			host = self.addHost('h%s' %h)
			switch = self.addSwitch('s%s' %h)
			self.addLink(host, switch)
			self.addLink(switch, entrySwitch)
	
		#Initialize clients conencted to the entry switch	
		for h in range (servers + 1, total + 1):
			host = self.addHost('h%s' %h)
			self.addLink(host, entrySwitch)

def StartScripts(servers, normal, malicious, maliciousInterval, connectScript, controllerIP):
	total = normal + malicious + servers
	firstNormal = servers + 1
	firstMalicious = firstNormal + normal
	topo = RoundRobinTopo(servers, total)
	net = Mininet(topo, controller=lambda name:RemoteController(name, defaultIP='127.0.0.1'), listenPort=6633)
	net.start()
	
	#Start the HTTP server on hosts
	for h in range (1, firstNormal):
		host = net.get('h%s' %h)
		host.cmd('python -m SimpleHTTPServer 80 &')
	
	#Allow time for the hosts to setup their server
	sleep(5)
	
	#Make intial connections to from a single host
	host = net.get('h%s' %firstNormal)
	for n in range (1, servers + 1):
		host.cmd('wget -b -O /dev/null -o /dev/null 10.0.%s.%s' %((n//256), (n%256)))
	
	#Loop through start randomConnect in background on normal hosts
	for n in range (firstNormal, firstMalicious):
		host = net.get('h%s' %n)
		host.cmd('./%s &' %connectScript)

	#Loop through each malicious host and send requests in groups after a delay
	counter = firstMalicious
	while counter < total:
		for n in range (1, servers):
			tmp = counter%malicious
			tmp += firstMalicious
			host = net.get('h%s' %tmp)
			host.cmd('wget -b -O /dev/null -o /dev/null %s' %controllerIP)
			counter += 1
		sleep(maliciousInterval)

	#net.interact()
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	#hosts are named starting at 1 with servers first, then normal clients, and finally malicious clients
	servers = 12
	normalClients = 100 
	maliciousClients = 200 	#ideally this should be a multiple of (servers - 1)
	maliciousInterval = .2
	connectScript = "randomConnect.sh"
	controllerIP = "10.255.0.100"	
	StartScripts(servers, normalClients, maliciousClients, maliciousInterval, connectScript, controllerIP)
