#! /usr/bin/python
#  coding: utf-8

"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""
import sys
import os
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import lg

from mininet.node import Node
from mininet.topolib import TreeNet

#################################
def startNAT( root, inetIntf='eth0', subnet='10.0/8' ):
    """Start NAT/forwarding between Mininet and external network
    root: node to access iptables from
    inetIntf: interface for internet access
    subnet: Mininet subnet (default 10.0/8)="""

    # Identify the interface connecting to the mininet network
    localIntf =  root.defaultIntf()

    # Flush any currently active rules
    root.cmd( 'iptables -F' )
    root.cmd( 'iptables -t nat -F' )

    # Create default entries for unmatched traffic
    root.cmd( 'iptables -P INPUT ACCEPT' )
    root.cmd( 'iptables -P OUTPUT ACCEPT' )
    root.cmd( 'iptables -P FORWARD DROP' )

    # Configure NAT
    root.cmd( 'iptables -I FORWARD -i', localIntf, '-d', subnet, '-j DROP' )
    root.cmd( 'iptables -A FORWARD -i', localIntf, '-s', subnet, '-j ACCEPT' )
    root.cmd( 'iptables -A FORWARD -i', inetIntf, '-d', subnet, '-j ACCEPT' )
    root.cmd( 'iptables -t nat -A POSTROUTING -o ', inetIntf, '-j MASQUERADE' )

    # Instruct the kernel to perform forwarding
    root.cmd( 'sysctl net.ipv4.ip_forward=1' )

def stopNAT( root ):
    """Stop NAT/forwarding between Mininet and external network"""
    # Flush any currently active rules
    root.cmd( 'iptables -F' )
    root.cmd( 'iptables -t nat -F' )

    # Instruct the kernel to stop forwarding
    root.cmd( 'sysctl net.ipv4.ip_forward=0' )

def fixNetworkManager( root, intf ):
    """Prevent network-manager from messing with our interface,
       by specifying manual configuration in /etc/network/interfaces
       root: a node in the root namespace (for running commands)
       intf: interface name"""
    cfile = '/etc/network/interfaces'
    line = '\niface %s inet manual\n' % intf
    config = open( cfile ).read()
    if ( line ) not in config:
        print '*** Adding', line.strip(), 'to', cfile
        with open( cfile, 'a' ) as f:
            f.write( line )
    # Probably need to restart network-manager to be safe -
    # hopefully this won't disconnect you
    root.cmd( 'service network-manager restart' )

def connectToInternet( network, switch='s1', rootip='10.254', subnet='10.0/8'):
    """Connect the network to the internet
       switch: switch to connect to root namespace
       rootip: address for interface in root namespace
       subnet: Mininet subnet"""
    switch = network.get( switch )
    prefixLen = subnet.split( '/' )[ 1 ]

    # Create a node in root namespace
    root = Node( 'root', inNamespace=False )

    # Prevent network-manager from interfering with our interface
    fixNetworkManager( root, 'root-eth0' )

    # Create link between root NS and switch
    link = network.addLink( root, switch )
    link.intf1.setIP( rootip, prefixLen )

    # Start network that now includes link to root namespace
    network.start()

    # Start NAT and establish forwarding
    startNAT( root )

    # Establish routes from end hosts
    for host in network.hosts:
        host.cmd( 'ip route flush root 0/0' )
        host.cmd( 'route add -net', subnet, 'dev', host.defaultIntf() )
        host.cmd( 'route add default gw', rootip )

    return root
class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self, maxbw):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        server1 = self.addHost('v1')
        server2 = self.addHost('v2')

        client1 = self.addHost('c1')
        client2 = self.addHost('c2')

        self.addLink(s1,client1)
        self.addLink(s1,client2)


        self.addLink(s1,s3)





        self.addLink(s2,server1)
        self.addLink(s2,server2)

        self.addLink(s2,s3)

if __name__ == '__main__':
    #default
    maxbw = 1
    controller_ip = '10.0.2.15'
    if len(sys.argv) > 1:
        controller_ip = sys.argv[1]

    topos = { 'mytopo': ( lambda: MyTopo() ) }
    topos = MyTopo(maxbw)
    net = Mininet(topo=topos,  controller=lambda name:RemoteController(name, defaultIP='127.0.0.1'), listenPort=6633)
    #net.start()
    # Configure and start NATted connectivity
    rootnode = connectToInternet( net )
    print "*** Hosts are running and should have internet connectivity"
    print "*** Type 'exit' or control-D to shut down network"

    os.system("sudo ~/floodlight-qos-beta-master/apps/qos/qosmanager2.py -e")
    #os.system("sudo ~/floodlight-qos-beta-master/apps/qos/mininet-add-queues_modified2.py")

    for i in range(1,3):
        client = net.get('c'+str(i))
        server = net.get('v'+str(i))
        
        server.cmd('cd /home/mininet/floodlight-qos-beta-master/apps/qos/nweb')
        server.cmd('nohup ./nweb23_ubuntu_12_4_32 80 /home/mininet/floodlight-qos-beta-master/apps/qos/nweb/gen_files/ &')
        client.cmd('ping -c 1 ' + server.IP())
        #client.cmd('cd /home/mininet/floodlight-qos-beta-master/apps/qos/')
        #client.cmd('nohup ./process.sh convertRequest.txt ' + client.IP() + ' ' + controller_ip+ ' >> show_output.txt &')

    #client1 = net.get('c1')
    #client1.cmd('cd ~/floodlight-qos-beta-master/apps/qos')
    #client1.cmd('./process_fairness.sh 10.0.0.3 ' + client.IP() + ' ' + controller_ip + ' file20m_1.jpg &')

    #client2 = net.get('c2')
    #client2.cmd('cd ~/floodlight-qos-beta-master/apps/qos')
    #client2.cmd('./process_fairness.sh 10.0.0.4 ' + client.IP() + ' ' + controller_ip + ' file20m_2.jpg &')

    
    CLI( net )
    # Shut down NAT
    stopNAT( rootnode )
   
    #net.interact()
    net.stop()

# need to setup server by config file?
#    for x in range(1,6):
#        host = net.get('h%s' %x)
#        host.cmd('sudo /home/mininet/workspace/RequestDistributor/output/process.sh /home/mininet/workspace/RequestDistributor/output/ipfor%s.txt > /home/mininet/workspace/RequestDistributor/output/results/result_for_host%s.txt' %(x ,x))
    
