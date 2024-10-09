# Authors: Krisham Prasai, William Lucas, Alan Chen

import argparse
import iperf3
import time
import json

def run_client(ip, port, server_ip, test):
    # Initialize the iPerf3 client
    client = iperf3.Client()
    client.port = port
    #client.server_hostname = '0.0.0.0'
    client.server_hostname = server_ip
    client.duration = 60  # Set duration to 60 seconds

    #print(f'Starting iPerf3 client from {ip}:{port} to {client.server_hostname}:{port} using {test.upper()}\n')

    if test == 'tcp':
        client.protocol = 'tcp'
        result = client.run()
        #debug: print("CLIENT RESULT:", result)
        if result.error:
            print(f"Error: {result.error}")
        else:
            return json.dumps({
                'sent_bytes': result.sent_bytes if result.sent_bytes else 0,
                'received_bytes': result.received_bytes if result.received_bytes else 0,
                'error': result.error if result.error else None,
            })
    elif test == 'udp':
        client.protocol = 'udp'
        result = client.run()
        if result.error:
            print(f"Error: {result.error}")
        else:
            return json.dumps({
                'sent_bytes': result.sent_bytes if result.sent_bytes else 0,
                'received_bytes': result.received_bytes if result.received_bytes else 0,
                'error': result.error if result.error else None,
            })

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='iPerf3 Client Script')
    parser.add_argument('-ip', type=str, required=True, help='Client IP address')
    parser.add_argument('-port', type=int, required=True, help='Client port number')
    parser.add_argument('-server_ip', type=str, required=True, help='Server IP address')
    parser.add_argument('-test', type=str, choices=['tcp', 'udp'], required=True, help='Test type: tcp or udp')
    args = parser.parse_args()
    
    # Run client with parsed arguments
    result = run_client(args.ip, args.port, args.server_ip, args.test)
    
    # Print the JSON output
    print(result)


