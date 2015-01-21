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

    def __init__( self, num_server, num_client ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        switch_list = []

        # Add hosts and switches
        for i in range (0 , num_server):
            switch = self.addSwitch( 'switch' + str(i + 1) )
            server = self.addHost( 'server' + str(i + 1) )
            switch_list.append(switch)
            #add link between switch and server
            self.addLink(switch,server)

            for j in range (0, num_client):
                client = self.addHost( 'client' + str((i * num_client) + j + 1) )
                #add link between switch and client
                self.addLink(switch,client)

        for i in range (0, num_server):
            switch = switch_list[i]
            for j in range ( (i+1), num_server):
                next_switch = switch_list[j]
                self.addLink(switch, next_switch)

if __name__ == '__main__':
    
    #for arg in sys.argv:
    #    print arg
    num_server = 5
    num_client = 3
    if len(sys.argv)>2:
        print "number of servers = " + sys.argv[1]
        num_server = sys.argv[1]

    topos = { 'mytopo': ( lambda: MyTopo() ) }
    topos = MyTopo(num_server, num_client)
    net = Mininet(topo=topos, controller=lambda name:RemoteController(name, defaultIP='127.0.0.1'), listenPort=6633)
    net.start()

    # Do a ping sweep to identify all hosts and servers with controller
    #host1 = net.get('h1')
    #host2 = net.get('h2')
    #host1.cmd('ping -c1', host2.IP())
    for i in range (0, num_server, 2):
        server = net.get( 'server' + str(i+1) )
        next_server = net.get( 'server' + str((i+2)%num_server) )
        server.cmd('ping -c 1 ', next_server.IP())
        for j in range (0, num_client):
            client = net.get( 'client' + str((i*num_client)+j+1) )
            next_client = net.get( 'client' + str( ( ((i+1)%num_server) *num_client) +j+1 ) )
            client.cmd('ping -c 1 ',next_client.IP())

    #denote serverIPs are in range  10.0.0.x - 10.0.0.y  where x = (num_server*num_client)+1 and y = x + (numserver-1)
    #start webserver with port 80 and 
    for i  in range (0, num_server):
        server = net.get( 'server' + str(i+1) )
        server.cmd('~/nweb/nweb23_ubuntu_12_4_32 80 ~/nweb/web/')

    net.interact()

# need to setup server by config file?
#    for x in range(1,6):
#        host = net.get('h%s' %x)
#        host.cmd('sudo /home/mininet/workspace/RequestDistributor/output/process.sh /home/mininet/workspace/RequestDistributor/output/ipfor%s.txt > /home/mininet/workspace/RequestDistributor/output/results/result_for_host%s.txt' %(x ,x))
    
