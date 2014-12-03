#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import RemoteController
from time import sleep

class MassSetupTopo(Topo):
	def __init__(self, total):
		Topo.__init__(self)
	
		switch = self.addSwitch('s1')
	
		#Initialize servers and switches
		for h in range (1, total):
			host = self.addHost('h%s' %h)
			self.addLink(host, switch)
	
def StartScripts():
	topo = MassSetupTopo(300)
	net = Mininet(topo)
	net.start
	net.interact()
	net.stop()	

if __name__ == '__main__':
	setLogLevel('info')
	StartScripts()

