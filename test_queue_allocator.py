"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""
import sys
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')

        server1 = self.addHost('server1')
        server2 = self.addHost('server2')
        server3 = self.addHost('server3')
        server4 = self.addHost('server4')
        server5 = self.addHost('server5')
        server6 = self.addHost('server6')
        server7 = self.addHost('server7')
        server8 = self.addHost('server8')

        client1 = self.addHost('client1')
        client2 = self.addHost('client2')
        client3 = self.addHost('client3')
        client4 = self.addHost('client4')
        client5 = self.addHost('client5')
        client6 = self.addHost('client6')
        client7 = self.addHost('client7')
        client8 = self.addHost('client8')

        self.addLink(s1,server1)
        self.addLink(s1,server2)
        self.addLink(s1,client1)
        self.addLink(s1,client2)
        self.addLink(s1,s5)

        self.addLink(s2,server3)
        self.addLink(s2,server4)
        self.addLink(s2,client3)
        self.addLink(s2,client4)
        self.addLink(s2,s5)

        self.addLink(s3,server5)
        self.addLink(s3,server6)
        self.addLink(s3,client5)
        self.addLink(s3,client6)
        self.addLink(s3,s5)

        self.addLink(s4,server7)
        self.addLink(s4,server8)
        self.addLink(s4,client7)
        self.addLink(s4,client8)
        self.addLink(s4,s5)

if __name__ == '__main__':
    
    topos = { 'mytopo': ( lambda: MyTopo() ) }
    topos = MyTopo()
    net = Mininet(topo=topos, controller=lambda name:RemoteController(name, defaultIP='127.0.0.1'), listenPort=6633)
    net.start()

   
    net.interact()
    net.stop()

# need to setup server by config file?
#    for x in range(1,6):
#        host = net.get('h%s' %x)
#        host.cmd('sudo /home/mininet/workspace/RequestDistributor/output/process.sh /home/mininet/workspace/RequestDistributor/output/ipfor%s.txt > /home/mininet/workspace/RequestDistributor/output/results/result_for_host%s.txt' %(x ,x))
    
