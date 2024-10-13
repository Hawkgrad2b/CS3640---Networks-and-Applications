# Authors: Krisham Prasai, William Lucas, Alan Chen

import subprocess
import json
import matplotlib.pyplot as plt

def parse_results(filename, protocol):
    # Parse throughput from JSON results for the specified protocol.
    
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        # TCP/UDP throughput in Mbps
        if protocol.lower() == 'tcp':
            # Convert from bytes to megabits
            print((data['total_bytes_received'] * 8) / (10**6))
            return ((data['total_bytes_received'] * 8) / (10**6))  # Mbps
        elif protocol.lower() == 'udp':
            # Convert from bytes to megabits, assuming 'sent_bytes'
            print(((data['total_bytes_sent'] * 8) / (10**6)))
            return ((data['total_bytes_sent'] * 8) / (10**6))  # Mbps
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return 0
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {filename}.")
        return 0

def plot_results(bw_bottleneck_list, tcp_throughputs, udp_throughputs):    
    # Plot the TCP and UDP throughput results.

    plt.figure(figsize=(10, 6))

    print(f'bw_bottleneck_list: {bw_bottleneck_list}, length: {len(bw_bottleneck_list)}')
    print(f'tcp_throughputs: {tcp_throughputs}, length: {len(tcp_throughputs)}')
    print(f'udp_throughputs: {udp_throughputs}, length: {len(udp_throughputs)}')

    # Plot TCP throughput
    plt.plot(bw_bottleneck_list, tcp_throughputs, label='TCP Throughput', marker='o', color='b')

    # Plot UDP throughput
    plt.plot(bw_bottleneck_list, udp_throughputs, label='UDP Throughput', marker='o', color='r')

    # Add labels and title
    plt.xlabel('Bottleneck Bandwidth (Mbps)')
    plt.ylabel('Throughput (Mbps)')
    plt.title('TCP and UDP Throughput vs Bottleneck Bandwidth')
    
    # Show legend
    plt.legend()
    
    # Save the plot to a file
    plt.savefig('analysis.png')
    plt.show()

def main():
    # Define the bottleneck bandwidths to test
    bottleneck_bandwidths = [8, 32, 64]
    bw_other = 100  # Set this to 100Mbps for other links

    # Lists to store throughput results
    tcp_throughputs = []
    udp_throughputs = []

    # Iterate over each bottleneck bandwidth
    for bw_bottleneck in bottleneck_bandwidths:
        print(f'Testing with bottleneck bandwidth: {bw_bottleneck} Mbps')

        # Build the command to run network_bottleneck.py
        cmd = [
            'sudo', 'python3', 'network_bottleneck.py',
            '-bw_bottleneck', str(bw_bottleneck),
            '-bw_other', str(bw_other),
            '-time', '10'  # Run for 10 seconds
        ]

        # Execute the command
        subprocess.run(cmd)

        # Collect TCP and UDP results from the output files
        tcp_throughput = parse_results(f'output-tcp-{bw_bottleneck}-{bw_other}.json', 'TCP')
        udp_throughput = parse_results(f'output-udp-{bw_bottleneck}-{bw_other}.json', 'UDP')

        # Append the throughput to the lists
        tcp_throughputs.append(tcp_throughput)
        udp_throughputs.append(udp_throughput)

    # Plot the results
    plot_results(bottleneck_bandwidths, tcp_throughputs, udp_throughputs)

    # Write insights to observations.txt
    with open('observations.txt', 'w') as f:
        f.write("Observations about Network Performance:\n")
        f.write("1. TCP throughput scales more predictably with bandwidth compared to UDP.\n")
        f.write("2. UDP may suffer from packet loss at lower bandwidths, impacting performance.\n")
        f.write("3. High reliability of TCP may come at the cost of overhead, while UDP is lighter but less reliable.\n")

if __name__ == '__main__':
    main()


