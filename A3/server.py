# Authors: Krisham Prasai, William Lucas, Alan Chen

import argparse
import iperf3

def main():
    parser = argparse.ArgumentParser(description='iPerf3 Server Script')
    parser.add_argument('-ip', type=str, required=True, help='Server IP address')
    parser.add_argument('-port', type=int, required=True, help='Server port number')
    args = parser.parse_args()

    # Initialize the iPerf3 server
    server = iperf3.Server()
    server.bind_address = args.ip
    server.port = args.port

    print(f'Starting iPerf3 server on {args.ip}:{args.port}')

    # Run the server
    while True:
        result = server.run()
        if result.error:
            print(f'Error: {result.error}')
        else:
            print('Test completed')

if __name__ == '__main__':
    main()
