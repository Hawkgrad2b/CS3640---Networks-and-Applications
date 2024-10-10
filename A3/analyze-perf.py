# Authors: Krisham Prasai, William Lucas, Alan Chen

import subprocess
import json
import matplotlib.pyplot as plt

def parse_results(filename, protocol):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            # Extract total bytes received from the JSON data
            total_bytes_received = data.get('total_bytes_received', 0)
            duration = 60
            # Calculate throughput in Mbps
            throughput_mbps = (total_bytes_received * 8) / (duration * 1_000_000)  # Convert bytes to bits, then to Mbps
            return throughput_mbps
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return 0
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {filename}.")
        return 0

def plot_results(bw_bottleneck_list, tcp_throughputs, udp_throughputs):
    plt.figure()
    plt.plot(bw_bottleneck_list, tcp_throughputs, 'o-', label='TCP Throughput')
    plt.plot(bw_bottleneck_list, udp_throughputs, 's-', label='UDP Throughput')
    plt.xlabel('Bottleneck Bandwidth (Mbps)')
    plt.ylabel('Throughput (Mbps)')
    plt.title('TCP and UDP Throughput vs Bottleneck Bandwidth')
    plt.legend()
    plt.grid(True)
    plt.savefig('analysis.png')
    plt.show()

def main():
    # Define the bottleneck bandwidths to test
    bottleneck_bandwidths = [8, 32, 64]
    bw_other = 100  

    # Lists to store throughput results
    tcp_throughputs = []
    udp_throughputs = []

    # Iterate over each bottleneck bandwidth
    for bw_bottleneck in bottleneck_bandwidths:
        print(f'Bottleneck bandwidth: {bw_bottleneck} Mbps')

        # Build the command to run network_bottleneck.py
        cmd = [
            'sudo', 'python3', 'network_bottleneck.py',
            '--bw_bottleneck', str(bw_bottleneck),
            '--bw_other', str(bw_other),
            '--time', '10'  
        ]

        subprocess.run(cmd)

        # Collect TCP and UDP results
        tcp_filename = f'output-tcp-{bw_bottleneck}-{bw_other}.json'
        udp_filename = f'output-udp-{bw_bottleneck}-{bw_other}.json'

        tcp_throughput = parse_results(tcp_filename, 'TCP')
        udp_throughput = parse_results(udp_filename, 'UDP')

        # Append the throughput to the lists
        tcp_throughputs.append(tcp_throughput)
        udp_throughputs.append(udp_throughput)

    # Plot the results
    plot_results(bottleneck_bandwidths, tcp_throughputs, udp_throughputs)

if __name__ == '__main__':
    main()