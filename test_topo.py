"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftTopHost = self.addHost( 'h1' )
        leftMidHost = self.addHost( 'h2' )
        leftBotHost = self.addHost( 'h3' )
	extraHost = self.addHost( 'h4' )

        rightTopHost = self.addHost( 'h5' )
        rightMidHost = self.addHost( 'h6' )
        rightBotHost = self.addHost( 'h7' )

        leftSwitch = self.addSwitch('s1')
        rightSwitch = self.addSwitch('s2')

        # Add links
        self.addLink( leftTopHost, leftSwitch )
        self.addLink( leftMidHost, leftSwitch )
        self.addLink( leftBotHost, leftSwitch )
	self.addLink( extraHost, leftSwitch )

        self.addLink( rightTopHost, rightSwitch )
        self.addLink( rightMidHost, rightSwitch )
        self.addLink( rightBotHost, rightSwitch )

        self.addLink( leftSwitch, rightSwitch )


topos = { 'mytopo': ( lambda: MyTopo() ) }
