# cs3640-traceroute.py
# Implementing a basic traceroute program using ICMP Echo messages.

import socket
import dpkt
import sys
import argparse
import time

# Same as ping program
def make_icmp_socket(ttl, timeout):
    # Creates a raw socket for ICMP packets, setting the TTL and timeout
    try:
        raw_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        raw_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        raw_sock.settimeout(timeout)
        return raw_sock
    except Exception as e:
        print(f'Error creating raw_socket: {e}')
        sys.exit()

# Same as ping program
def send_icmp_echo(sock, payload, id, seq, destination):
    # Uses the dpkt module to craft and send an ICMP Echo packet
    icmp = dpkt.icmp.ICMP()
    icmp.type = dpkt.icmp.ICMP_ECHO
    icmp.code = 0
    icmp.data = dpkt.icmp.ICMP.Echo(id=id, seq=seq, data=payload.encode())
    icmp.pack()  # Computes checksum automatically

    try:
        sock.sendto(bytes(icmp), (destination, 0))
    except Exception as e:
        print(f'Error sending packet: {e}')

def recv_icmp_response(sock, id, timeout):
    # Receives ICMP response packets and checks if the packet is a Time Exceeded message
    start_time = time.time()
    try:
        packet, addr = sock.recvfrom(1024)
        end_time = time.time()

        # Parse ICMP type to see if it's a Time Exceeded message
        icmp_type = packet[20]  # The ICMP type field
        if icmp_type == 11: # ICMP Time Exceeded message
            rtt = (end_time - start_time) * 1000  # RTT in milliseconds
            return addr[0], rtt  # Return the IP address and RTT
        elif icmp_type == 0: # ICMP Echo Reply message
            rtt = (end_time - start_time) * 1000
            return addr[0], rtt  # Return IP and RTT if it's the final destination
    except socket.timeout:
        return None, None  # Timeout case
    except Exception as e:
        print(f"Error receiving packet: {e}")
        return None, None

def main():
    parser = argparse.ArgumentParser(description='Traceroute Program')
    parser.add_argument('-destination', required=True, help='Destination IP address')
    parser.add_argument('-n_hops', type=int, default=30, help='Maximum number of hops')
    args = parser.parse_args()

    # Set initial TTL and payload
    ttl = 1
    payload = "Traceroute message"

    while ttl <= args.n_hops:
        sock = make_icmp_socket(ttl, 1)  # Create a socket with current TTL
        send_icmp_echo(sock, payload, id=0, seq=ttl, destination=args.destination)
        
        ip, rtt = recv_icmp_response(sock, id=0, timeout=1)  # Receive the response
        
        if ip:
            print(f'destination = {args.destination}; hop {ttl} = {ip}; rtt = {rtt:.2f} ms')
            if ip == args.destination:
                print("Reached destination.")
                break
        else:
            print(f'destination = {args.destination}; hop {ttl} = *; rtt = * ms (timeout)')
        
        ttl += 1  # Increment TTL for the next hop
        sock.close()

if __name__ == '__main__':
    main()

