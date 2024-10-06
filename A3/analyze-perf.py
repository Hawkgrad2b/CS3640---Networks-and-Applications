# Authors: Krisham Prasai, William Lucas, Alan Chen

import subprocess
import json
import matplotlib.pyplot as plt

def parse_results(filename, protocol):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)


def plot_results(bw_bottleneck_list, tcp_throughputs, udp_throughputs):
    pass 

def main():
    # Define the bottleneck bandwidths to test
    bottleneck_bandwidths = [8, 32, 64]
    bw_other = 100  

    # Lists to store throughput results
    tcp_throughputs = []
    udp_throughputs = []

    # Iterate over each bottleneck bandwidth
    for bw_bottleneck in bottleneck_bandwidths:
        print(f'bottletynck bandwidth: {bw_bottleneck} Mbps')

        # Build the command to run network_bottleneck.py
        cmd = [
            'sudo', 'python3', 'network_bottleneck.py',
            '--bw_bottleneck', str(bw_bottleneck),
            '--bw_other', str(bw_other),
            '--time', '10'  
        ]

        subprocess.run(cmd)

        # Collect TCP and UDP results
        tcp_throughput = parse_results(f'output-tcp-{bw_bottleneck}-{bw_other}.json', 'TCP')
        udp_throughput = parse_results(f'output-udp-{bw_bottleneck}-{bw_other}.json', 'UDP')

        # Append the throughput to the lists
        tcp_throughputs.append(tcp_throughput)
        udp_throughputs.append(udp_throughput)

    # Plot the results
    plot_results(bottleneck_bandwidths, tcp_throughputs, udp_throughputs)


