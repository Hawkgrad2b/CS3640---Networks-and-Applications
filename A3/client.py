# Authors: Krisham Prasai, William Lucas, Alan Chen

import argparse
import iperf3

def main():
    parser = argparse.ArgumentParser(description='iPerf3 Client Script')
    parser.add_argument('-ip', type=str, required=True, help='Client IP address')
    parser.add_argument('-port', type=int, required=True, help='Client port number')
    parser.add_argument('-server_ip', type=str, required=True, help='Server IP address')
    parser.add_argument('-test', type=str, choices=['tcp', 'udp'], required=True, help='Test type: tcp or udp')
    args = parser.parse_args()

    # Initialize the iPerf3 client
    client = iperf3.Client()
    client.bind_address = args.ip
    client.port = args.port
    client.server_hostname = args.server_ip
    client.duration = 60  # Set duration to 60 seconds
    client.json_output = True

    if args.test == 'tcp':
        client.protocol = 'tcp'
    elif args.test == 'udp':
        client.protocol = 'udp'

    print(f'Starting iPerf3 client from {args.ip}:{args.port} to {args.server_ip}:{args.port} using {args.test.upper()}')

    # Run the client test
    result = client.run()

    if result.error:
        print(f'Error: {result.error}')
    else:
        # Save the result as a JSON file
        filename = f'output-{args.test}-{args.ip}-{args.server_ip}.json'
        with open(filename, 'w') as f:
            f.write(result.text)
        print(f'Results saved to {filename}')

if __name__ == '__main__':
    main()
