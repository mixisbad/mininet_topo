#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import RemoteController
from time import sleep


class SimpleTopo(Topo):
	def __init__(self):
		Topo.__init__(self)
		
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')	
		self.addLink(s1, s2)
		h1 = self.addHost('h1')
		h2 = self.addHost('h2')
		self.addLink(h1, s1)
		self.addLink(h2, s2)


def StartScripts():
	topo = SimpleTopo()
	net = Mininet(topo)
	net.start()
	net.interact()
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	StartScripts()

