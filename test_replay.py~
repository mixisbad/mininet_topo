"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
	h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        h3 = self.addHost( 'h3' )

	h4 = self.addHost( 'h4' )
        h5 = self.addHost( 'h5' )
        h6 = self.addHost( 'h6' )


	s1 = self.addSwitch( 's1' )
	s2 = self.addSwitch( 's2' )
	s3 = self.addSwitch( 's3' )
        s4 = self.addSwitch( 's4' )


        # Add links
        self.addLink( h1, s1 )
        self.addLink( h2, s1 )
        self.addLink( h3, s1 )


	self.addLink( h4, s4 )
        self.addLink( h5, s4 )
        self.addLink( h6, s4 )

	self.addLink( s1, s2 )
	self.addLink( s1, s3 )
        self.addLink( s1, s4 )

        self.addLink( s2, s4 )

	self.addLink( s3, s4 )

if __name__ == '__main__':
    #topos = { 'mytopo': ( lambda: MyTopo() ) }
    topos = MyTopo()
    net = Mininet(topo=topos, controller=lambda name:RemoteController(name, defaultIP='127.0.0.1'), listenPort=6633)
    net.start()

    # Do a ping sweep to identify all hosts with controller
    host1 = net.get('h1')
    host2 = net.get('h2')
    host1.cmd('ping -c1', host2.IP())

    host1 = net.get('h3')
    host2 = net.get('h4')
    host1.cmd('ping -c1', host2.IP())

    host1 = net.get('h5')
    host2 = net.get('h6')
    host1.cmd('ping -c1', host2.IP())

    for x in range(1,6):
        host = net.get('h%s' %x)
        host.cmd('sudo /home/mininet/workspace/RequestDistributor/output/process.sh /home/mininet/workspace/RequestDistributor/output/ipfor%s.txt > /home/mininet/workspace/RequestDistributor/output/results/result_for_host%s.txt' %(x ,x))
    
