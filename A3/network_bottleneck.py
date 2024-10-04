# Authors: Krisham Prasai, William Lucas, Alan Chen
# Setup a simple network topology using two client nodes, two server nodes,
# and two switches using Mininet

# use for clearing mininet state
import os

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
        # added parameters for limiting the rate-to-quantum variable
        self.addLink(h1, s1, bw=bw_other, cls=TCLink)
        self.addLink(h2, s1, bw=bw_other, cls=TCLink)
        
        self.addLink(s1, s2, bw=bw_bottleneck, cls=TCLink) # bottlneck link
        self.addLink(s2, h3, bw=bw_other, cls=TCLink)
        self.addLink(s2, h4, bw=bw_other, cls=TCLink)
        

def run_topology_tests(bw_bottleneck, bw_other):
    #in progress (-wplucas)
    topo = BottleNeckTopology(bw_bottleneck, bw_other)
    net = Mininet(topo=topo, link=TCLink)

    # Start the network
    net.start()

    # Record passed in parameters
    with open('output-network-config.txt', 'w') as f:
        f.write(f'bottleneck bandwith: {bw_bottleneck} Mbps\n')
        f.write(f'Other links bandwith: {bw_other} Mbps\n')

    # Get the two client nodes
    h1 = net.get('h1')
    h2 = net.get('h2')

    # Get the two server nodes
    h3 = net.get('h3')
    h4 = net.get('h4')

    hosts = [h1,h2,h3,h4]

    # For each host, use the ifconfig command and record results
    for index, host in enumerate(hosts, 1):
        ifconfig_results = host.cmd('ifconfig')
        with open(f"output-ifconfig-h{index}.txt", 'w' ) as f:
            f.write(ifconfig_results)

    # For each host, use the ping command and record results
    for index, host in enumerate(hosts, 1):
        ping_result = f'host {index}:\n'
        for target_host in hosts:
            if host != target_host:
                ping_result += host.cmd(f'ping -c 4 {target_host.IP()}')

        with open(f"output-ping-h{index}.txt", 'w') as f:
            f.write(ping_result + '\n')

    # Stop network after all tests have been run 
    return net

#
def run_pref_tests():
    pass

if __name__ == "__main__":
    # Clearing mininet state between executions
    os.system('sudo mn -c')
    
    # Intialize the argparse parser to take the command-line args
    parser = argparse.ArgumentParser(description="Network Bottleneck parser")

    # Define the arguments, 
    # bandwidth (for bottleneck link and other links) and time
    parser.add_argument('-bw_bottleneck', type=int, default=10,
                        help='Bandwidth (Mbps) for the bottleneck link (default is 10Mbps)')
    parser.add_argument('-bw_other', type=int, default=100,
                        help='Bandwidth (Mbps) for other links (default is 100Mbps)')
    parser.add_argument('-time', type=int, default=10,
                        help='Duration (seconds) of traffic simulation. (default is 10 seconds)')
    
    args = parser.parse_args()

    if args.bw_other <= args.bw_bottleneck:
        raise ValueError('The bandwidth for other links must be higher than the ' +
                         'specified bottleneck bandwidth')
    
    net = run_topology_tests(args.bw_bottleneck, args.bw_other)

    run_perf_tests(net, bottleneck_bw, other_bw)

    net.stop()
