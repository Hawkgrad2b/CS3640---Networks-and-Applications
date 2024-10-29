# Implementing a basic ping program using ICMP Echo messages.
# Measuring the reachability of a destination host and its RTT.
# This file will send and recieve ICMP messages and responses.
# IT will display the RTT for each packet sent and recieved,
# along with a summary of the avg RTT and success rate.

import socket
import dpkt
import sys
import argparse
import time
import logging
import random

logging.basicConfig(
    filename='cs3640-ping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def resolve_ip(ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        logging.info("IP address succesfully resolved to hostname")
        return hostname
    except socket.herror as e:
        logging.error("Could not resolve ip to hostname: %s", e)
        return None
    
def make_icmp_socket(ttl, timeout):
    # Creats a raw scoket for ICMP packets, sets the TTL and timeout
    # socket.IPPROTO_ICMP specifies that socket uses ICMP
    try:
        raw_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        raw_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        raw_sock.settimeout(timeout)
        logging.info("ICMP Socket created with TTL=%d and timeout=%d", ttl, timeout)
        return raw_sock
    except Exception as e:
        print(f'Error creating raw_socket: {e}')
        logging.error("Error creating raw socket: %s", e)
        sys.exit()

def send_icmp_echo(socket, payload, id, seq, destination):
    # Uses the dpkt module
    # Crafts and sends ICMP Echo packet
    # Payload, ID, and seq num set based on input
    # Packet sent to destination via input socket

    # Create ICMP Echo Request packet using dpkt
    icmp = dpkt.icmp.ICMP()
    icmp.type = dpkt.icmp.ICMP_ECHO
    icmp.code = 0
    icmp.data = dpkt.icmp.ICMP.Echo(id=id, seq=seq, data=payload.encode())
    icmp.pack() # Computes checksum automatically

    try:
        # Send packet to dest
        socket.sendto(bytes(icmp), (destination, 0))
        logging.info("Sent ICMP echo to %s; id=%d, seq=%d", destination, id, seq)
    except Exception as e:
        print(f'Error sending packet: {e}')
        logging.error("Error sending packet to %s: %s", destination, e)


def recv_icmp_response(socket, id, timeout):
    # Creates a raw socket for receiving ICMP responses 
    # Waits for an incoming echo response, returned to caller
    start_time = time.time()

    try:
        packet, addr = socket.recvfrom(1024)
        end_time = time.time()

        # Use dpkt to parse the ICMP response
        icmp = dpkt.icmp.ICMP(packet[20:]) # ICMP header starts after the IP header
        if isinstance(icmp.data, dpkt.icmp.ICMP.Echo):
            if icmp.data.id == id:
                rtt = (end_time - start_time) * 1000  # Convert to milliseconds
                logging.info("Received response from %s; RTT=%.1f ms", addr[0], rtt)
                return rtt, addr[0]  # Return RTT and source address

    except socket.timeout:
        logging.warning("Request timed out for id=%d", id)
        return None, None
    except Exception as e:
        print(f"Error receiving or parsing packet: {e}")
        logging.error("Error receiving or parsing packet: %s", e)
        return None, None

def main():
    parser = argparse.ArgumentParser(description='Ping a host using ICMP Echo messages.')
    parser.add_argument('-destination', type=str, required=True, help='The destination IP address')
    parser.add_argument('-n', type=int, required=True, help='Number of packets to send')
    parser.add_argument('-ttl', type=int, default=64, help='Time to live for packets')
    args = parser.parse_args()

    try:
        socket.inet_aton(args.destination)
    except socket.error as e:
        print(f"Invalid destination IP address: {e}")
        logging.error("Invalid destination IP address: %s", e)

    logging.info("Starting ping to %s with %d packets and TTL=%d", args.destination, args.n, args.ttl)

    # Create ICMP socket
    sock = make_icmp_socket(args.ttl, 1)

    total_rtt = 0
    successful_pings = 0

    for seq in range(args.n):
        id = seq  # Use seq number as id for simplicity
        payload = 'Ping'  # Simple payload

        send_icmp_echo(sock, payload, id, seq, args.destination)

        response = recv_icmp_response(sock, id, 1)
        if response:
            rtt, src_address = response
            print(f'destination = {args.destination}; icmp_seq = {seq}; icmp_id = {id}; ttl = {args.ttl}; rtt = {rtt:.1f} ms')
            total_rtt += rtt
            successful_pings += 1
        else:
            print(f'destination = {args.destination}; icmp_seq = {seq}; icmp_id = {id}; ttl = {args.ttl}; Request timed out.')

    if successful_pings > 0:
        avg_rtt = total_rtt / successful_pings
        print(f'Average rtt: {avg_rtt:.1f} ms; {successful_pings}/{args.n} successful pings.')
        logging.info("Ping Complete: Average RTT=%.1f ms, %d/%d successful pings", avg_rtt, successful_pings, args.n)
    else:
        print('No successful pings.')
        logging.warning("No successful pings to %s", args.destination)

if __name__ == '__main__':
    main()

