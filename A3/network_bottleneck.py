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


