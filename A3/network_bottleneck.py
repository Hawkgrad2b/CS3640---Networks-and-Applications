# Authors: Krisham Prasai, William Lucas, Alan Chen
# Setup a simple network topology using two client nodes, two server nodes,
# and two switches using Mininet

# use argparse to handle command-line arguments
import argparse

# use subprocess to use system commands like 'ifconfig' and 'ping'
import subprocess

# import all necessary Mininet modules
from mininet.net import Mininet # core to create network
from mininet.node import Node, OVSSwitch # nodes (hosts, switches)
from mininet.topo import Topo # define network topology
from mininet.link import TCLink # traffic control links (set bandwidth limits)
from mininet.log import setLogLevel # for logging information
from mininet.util import dumpNodeConnections # dump connections between nodes

class BottleNeckTopology(Topo):

    def build(self, bw_bottleneck, bw_other):
        # adding two client nodes
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        # adding two server nodes
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        # addings the two switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # add the links connecting the devices
        self.addLink(h1, s1, bw=bw_other)
        self.addLink(h2, s1, bw=bw_other)
        self.addLink(s1, s2, bw=bw_bottleneck) # bottlneck link
        self.addLink(s2, h3, bw=bw_other)
        self.addLink(s2, h4, bw=bw_other)


def Create_Network(bw_bottleneck, bw_other, sim_time):
    #in progress (-wplucas)
    topo = BottleNeckTopology()
    net = Mininet(Topo= topo, link= TCLink)

    net.start()

    net.stop()




if __name__ == "__main__":
    # Intialize the argparse parser to take the command-line args
    parser = argparse.ArgumentParser(description="Network Bottleneck parser")

    # Define the arguments, 
    # bandwidth (for bottleneck link and other links) and time
    parser.add_argument('-bw_bottleneck', type=int, default=10,
                        help='Bandwidth (Mbps) for the bottleneck link (default is 10Mbps)')
    parser.add_argument('bw_other', type=int, default=100,
                        help='Bandwidth (Mbps) for other links (default is 100Mbps)')
    parser.add_argument('-time', type=int, default=10,
                        help='Duration (seconds) of traffic simulation. (default is 10 seconds)')
    
    args = parser.parse_args()

    if args.bw_other <= args.bw_bottleneck:
        raise ValueError('The bandwidth for other links must be higher than the ' +
                         'specified bottleneck bandwidth')
    
    Create_Network(args.bw_bottleneck, args.bw_other, args.time)


