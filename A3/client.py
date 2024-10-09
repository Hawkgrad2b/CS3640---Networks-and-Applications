# Authors: Krisham Prasai, William Lucas, Alan Chen

import argparse
import iperf3
import time
# import json

def run_client(server_ip, port, test):
    # Initialize the iPerf3 client
    client = iperf3.Client()
    # client.bind_address = args.ip
    client.port = port
    client.server_hostname = server_ip
    client.duration = 60  # Set duration to 60 seconds

    print(f'Starting iPerf3 client from {args.ip}:{args.port} to {args.server_ip}:{args.port} using {args.test.upper()}\n')

    if test == 'tcp':
        client.protocol = 'tcp'
        result = client.run()
        return {
            'sent_bytes': result.sent_bytes,
            'received_bytes': result.received_bytes,
        }
    elif test == 'udp':
        client.protocol = 'udp'
        result = client.run()
        return {
            'sent_bytes': result.sent_bytes,
            'received_bytes': result.received_bytes,
        }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='iPerf3 Client Script')
    parser.add_argument('-ip', type=str, required=True, help='Client IP address')
    parser.add_argument('-port', type=int, required=True, help='Client port number')
    parser.add_argument('-server_ip', type=str, required=True, help='Server IP address')
    parser.add_argument('-test', type=str, choices=['tcp', 'udp'], required=True, help='Test type: tcp or udp')
    args = parser.parse_args()

    result = run_client(args.server_ip, args.port, args.test)
    print(result)


