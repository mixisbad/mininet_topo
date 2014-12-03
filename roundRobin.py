#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import RemoteController
from time import sleep

class RoundRobinTopo(Topo):
	"""Host1 with server -- Switch \
                                        \                /--- Client host4
                                         \              /
                                          \            /
           Host2 with server -- Switch ----- Switch ----- --- Client host5
                                          /            \
                                         /              \
                                        /                \--- Client host6
           Host3 with server -- Switch / """

	def __init__(self):
		Topo.__init__(self)
		
		#Initialize hosts and switchs
		TopServer = self.addHost('h1')
		MiddleServer = self.addHost('h2')
		BottomServer = self.addHost('h3')
		TopClient = self.addHost('h4')
		MiddleClient = self.addHost('h5')
		BottomClient = self.addHost('h6')
		TopSwitch = self.addSwitch('s1')
		MiddleSwitch = self.addSwitch('s2')
		BottomSwitch = self.addSwitch('s3')
		EndSwitch = self.addSwitch('s4')

		#Add links
		self.addLink(TopServer, TopSwitch)
		self.addLink(MiddleServer, MiddleSwitch)
		self.addLink(BottomServer, BottomSwitch)
		self.addLink(TopSwitch, EndSwitch)
		self.addLink(MiddleSwitch, EndSwitch)
		self.addLink(BottomSwitch, EndSwitch)
		self.addLink(EndSwitch, TopClient)
		self.addLink(EndSwitch, MiddleClient)
		self.addLink(EndSwitch, BottomClient)

def StartScripts():
	topo = RoundRobinTopo()
	net = Mininet(topo, controller=lambda name:RemoteController(name, deafultIP='127.0.0.1'), listenPort=6633)
	net.start()
	h1, h2, h3 = net.get('h1', 'h2', 'h3')
	#h1.cmd('./wget.sh')
	h1.cmd('python -m SimpleHTTPServer 80 &')
	h2.cmd('python -m SimpleHTTPServer 80 &')
	h3.cmd('python -m SimpleHTTPServer 80 &')
	sleep(5)
	h4, h5, h6 = net.get('h4', 'h5', 'h6')
	h4.cmd('wget -O - 10.0.0.1')
	h4.cmd('wget -O - 10.0.0.2')
	h4.cmd('wget -O - 10.0.0.3')	
	h4.cmd('./randomConnect.sh &')
	h5.cmd('./randomConnect.sh &')
	h6.cmd('./randomConnect.sh &')	
	net.interact()
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	StartScripts()


