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

def make_icmp_socket(ttl, timeout):
    # Creats a raw scoket for ICMP packets, sets the TTL and timeout
    # socket.IPPROTO_ICMP specifies that socket uses ICMP
    try:
        raw_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        raw_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        raw_sock.settimeout(timeout)

    except Exception as e:
        print(f'Error creating raw_socket: {e}')
        sys.exit()

def send_icmp_echo(socket, payload, id, seq, destination):
    # uses the dpkt module
    # crafts and sends ICMP Echo packet
    # payload, ID, and seq num set based on input
    # packet sent to destination via input socket

    # Create ICMP Echo Request packet using dpkt
    icmp = dpkt.icmp.ICMP()
    icmp.type = dpkt.icmp.ICMP_ECHO
    icmp.code = 0
    icmp.data = dpkt.icmp.TCMP.Echo(id=id, seq=seq, data=payload.encode())
    icmp.pack() # Computes checksum automatically

    # Send packet to dest
    socket.sendto(bytes(icmp), (destination, 0))


def recv_icmp_response(socket, id, timeout):
    # creates a raw socket for recieving ICMP responses 
    # waits for an incoming echo response, returned to caller
    start_time = time.time()

    try:
        packet, addr = socket.recvfrom(1024)
        end_time = time.time()

        # Use dpkt to parse the ICMP response?

        
    except socket.timeoout:
        return None

    return

# Create a program that sends ICMP Echo packets to dest and saves RTT for each packet.
# ID and Seq num start at 0 and ++ by 1 w/ each packet sent.
# program sends 'n' packets, cmd-line arg.
# TTL should be configurable via cmd-line arg
# output should display RTT for each packet w/ summary & success rate
# ex ( $ python3 cs3640-ping.py -destination 8.8.8.8 -n 3 -ttl 100 returns:
# destination = 8.8.8.8; icmp_seq = 0; icmp_id = 0; ttl = 100; rtt = 14.0 ms
# destination = 8.8.8.8; icmp_seq = 1; icmp_id = 1; ttl = 100; rtt = 14.2 ms
# destination = 8.8.8.8; icmp_seq = 2; icmp_id = 2; ttl = 100; rtt = 14.5 ms
# Average rtt: 14.2 ms; 3/3 successful pings.
