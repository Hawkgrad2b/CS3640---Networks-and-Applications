# Authors: Krisham Prasai, William Lucas, Alan Chen

import argparse
import iperf3
import json

def main():
    parser = argparse.ArgumentParser(description='iPerf3 Client Script')
    parser.add_argument('-ip', type=str, required=True, help='Client IP address')
    parser.add_argument('-port', type=int, required=True, help='Client port number')
    parser.add_argument('-server_ip', type=str, required=True, help='Server IP address')
    parser.add_argument('-test', type=str, choices=['tcp', 'udp'], required=True, help='Test type: tcp or udp')
    args = parser.parse_args()

    # Initialize the iPerf3 client
    client = iperf3.Client()
    # client.bind_address = args.ip
    client.port = args.port
    client.server_hostname = args.server_ip
    client.duration = 60  # Set duration to 60 seconds
    client.json_output = True # Configure to be saved to JSON

    if args.test == 'tcp':
        client.protocol = 'tcp'
    elif args.test == 'udp':
        client.protocol = 'udp'

    print(f'Starting iPerf3 client from {args.ip}:{args.port} to {args.server_ip}:{args.port} using {args.test.upper()}\n')

    # Running the client test
    result = client.run()

    if result.error:
        print(f'Error: {result.error}')
    else:
        # Save the result as a JSON file using json.dump
        filename = f'output-{args.test}-{args.ip}-{args.server_ip}.json'
        with open(filename, 'w') as f:
            json.dump(result.json, f, indent=4)
        print(f'Results saved to {filename}\n')

if __name__ == '__main__':
    main()

