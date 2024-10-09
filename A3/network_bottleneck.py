# Authors: Krisham Prasai, William Lucas, Alan Chen
# Setup a simple network topology using two client nodes, two server nodes,
# and two switches using Mininet

import os
import time
import json
import argparse
import subprocess
import iperf3
from mininet.net import Mininet # core to create network
from mininet.topo import Topo # define network topology
from mininet.link import TCLink # traffic control links (set bandwidth limits)

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
        self.addLink(h1, s1, bw=bw_other, cls=TCLink)
        self.addLink(h2, s1, bw=bw_other, cls=TCLink)
        
        self.addLink(s1, s2, bw=bw_bottleneck, cls=TCLink) # bottlneck link
        self.addLink(s2, h3, bw=bw_other, cls=TCLink)
        self.addLink(s2, h4, bw=bw_other, cls=TCLink)
        

def run_topology_tests(bw_bottleneck, bw_other):
    # Build the topology and start the network
    topo = BottleNeckTopology(bw_bottleneck, bw_other)
    net = Mininet(topo=topo, link=TCLink, controller=None)
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

        # write results to specific ping text file 
        with open(f"output-ping-h{index}.txt", 'w') as f:
            f.write('\n' + ping_result)

    # Stop network after all tests have been run 
    return net

def run_perf_tests(net, bw_bottleneck, bw_other):
    #Get the client and server nodes
    h1 = net.get('h1') # TCP client
    h2 = net.get('h2') # UDP client
    h3 = net.get('h3') # TCP server
    h4 = net.get('h4') # UDP server 

    client_tcp_ip = h1.IP()
    client_udp_ip = h2.IP()
    server_tcp_ip = h3.IP()
    server_udp_ip = h4.IP()
    
    # TCP SETUP-----------------
    server_tcp_cmd = f'sudo python3 server.py -ip {server_tcp_ip} -port 5001'
    try:
        tcp_server_start = subprocess.Popen(server_tcp_cmd, shell=True)
    except Exception as e:
        print(f'Error: {e}')
        tcp_server_start.terminate()
        exit(1)
    time.sleep(2)

    tcp_client_cmd = f'sudo python3 client.py -ip {client_tcp_ip} -port 5001 -server_ip {server_tcp_ip} -test tcp'
    tcp_result = subprocess.Popen(tcp_client_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for the client to complete and fetch its output
    tcp_output, tcp_error = tcp_result.communicate()
    tcp_server_start.terminate()
    if tcp_error:
        print(f"TCP client error: {tcp_error.decode()}")

    # Extract data from TCP result
    try:
        tcp_data = json.loads(tcp_output.decode().strip())
    except Exception as e:
        print("Failed to decode JSON:", e)
        print("TCP Output:", tcp_output.decode().strip())
        exit(1) # Terminate whole script

    total_bytes_sent_tcp = tcp_data.get('sent_bytes', 0)
    total_bytes_received_tcp = tcp_data.get('received_bytes', 0)
    
    # Create and write to the TCP output JSON file
    tcp_output_filename = f'output-tcp-{bw_bottleneck}-{bw_other}.json'
    tcp_output_data = {
        'test_type': 'TCP',
        'bottleneck_bandwidth': bw_bottleneck,
        'other_bandwidth': bw_other,
        'total_bytes_sent': total_bytes_sent_tcp,
        'total_bytes_received': total_bytes_received_tcp
    }
    with open(tcp_output_filename, 'w') as f:
        json.dump(tcp_output_data, f, indent=4)
    print(f'TCP results written to {tcp_output_filename}')

    
    # UDP SETUP-----------------
    server_udp_cmd = f'sudo python3 server.py -ip {server_udp_ip} -port 5002'
    try:
        udp_server_start = subprocess.Popen(server_udp_cmd, shell=True)
    except Exception as e:
        print(f'Error: {e}')
        tcp_server_start.terminate()
        exit(1)
    time.sleep(2)

    udp_client_cmd = f'sudo python3 client.py -ip {client_udp_ip} -port 5002 -server_ip {server_udp_ip} -test udp'
    udp_result = subprocess.Popen(udp_client_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for client to complete and fetch
    udp_output, udp_error = udp_result.communicate()
    udp_server_start.terminate()
    if udp_error:
        print(f"UDP client error: {udp_error.decode()}")
    
    # Extract data from UDP result
    try:
        udp_data = json.loads(udp_output.decode().strip())
    except Exception as e:
        print("Failed to decode JSON:", e)
        print("UDP Output:", tcp_output.decode().strip())
        exit(1) #Terminate whole script
    
    total_bytes_sent_udp = udp_data.get('sent_bytes', 0)
    total_bytes_received_udp = udp_data('received_bytes', 0)
    
    # Create and write to the UDP output JSON file
    udp_output_filename = f'output-udp-{bw_bottleneck}-{bw_other}.json'
    udp_output_data = {
        'test_type': 'UDP',
        'bottleneck_bandwidth': bw_bottleneck,
        'other_bandwidth': bw_other,
        'total_bytes_sent': total_bytes_sent_udp,
        'total_bytes_received': total_bytes_received_udp
    }
    with open(udp_output_filename, 'w') as f:
        json.dump(udp_output_data, f, indent=4)
    print(f'UDP results written to {udp_output_filename}')


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

    run_perf_tests(net, args.bw_bottleneck, args.bw_other)

    net.stop()
