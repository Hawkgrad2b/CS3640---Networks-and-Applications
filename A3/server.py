# Authors: Krisham Prasai, William Lucas, Alan Chen

import argparse
import iperf3
import time

def main():
    parser = argparse.ArgumentParser(description='iPerf3 Server Script')
    parser.add_argument('-ip', type=str, required=True, help='Server IP address')
    parser.add_argument('-port', type=int, required=True, help='Server port number')
    args = parser.parse_args()

    # Initialize the iPerf3 server
    server = iperf3.Server()
    #server.bind_address = '0.0.0.0' # due to binding issue, 10.0.0.x doesnt work
    server.bind_address = args.ip
    server.port = args.port

    # print(f'Starting iPerf3 server on {server.bind_address} :{args.port}\n')

    # Run the server
    max_tries = 5
    for attempt in range(max_tries):
        result = server.run()
        if result.error:
            print(f'Error on attempt {attempt + 1}: {result.error}\n')
            time.sleep(1)
        else:
            print('Test completed\n')
            break
    else:
        print('Max attempts reached. Exiting.')

if __name__ == '__main__':
    main()
