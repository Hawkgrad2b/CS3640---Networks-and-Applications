# Network Tools Implementation Assignment

**Instructor:** Rishab Nithyanand  
**TA:** Jack Clisham  
**Code Authored by:**  
- Alan Chen (HawkID: alachen)  <br>
- William Lucas (HawkID: wplucas)  <br>
- Krisham Prasai (HawkID: kprasai)  <br>
- Vinayak Deshpande (HawkID: vdeshpande) <br>

This project involves implementing network tools in Python, including a Ping program, a Traceroute program, and an Intelligence Server and Client. The assignment is divided into three tasks:

1. **Implementing the Ping Program (`cs3640-ping.py`)**
2. **Implementing the Traceroute Program (`cs3640-traceroute.py`)**
3. **Implementing the Intelligence Server and Client (`cs3640-intelserver.py` and `cs3640-intelclient.py`)**
## Install Required Python Modules
~~~
pip3 install dpkt dnspython pyOpenSSL ipwhois
~~~
## Task 1: Implementing the Ping Program

### Description
Create a Python program `cs3640-ping.py` that sends ICMP Echo messages to a destination host and measures the RTT for each packet. The program should:

- **Define three main methods:**
  - `make_icmp_socket(ttl, timeout)`: Creates a raw socket for ICMP packets with the specified TTL and timeout.
  - `send_icmp_echo(socket, payload, id, seq, destination)`: Crafts and sends an ICMP Echo packet using the `dpkt` module.
  - `recv_icmp_response()`: Waits for an incoming ICMP Echo response and returns it to the caller.
- **Send** `n` **packets to the destination**, where `n` is a command-line argument.
- **Use IDs and sequence numbers starting from 0**, incrementing by 1 with each packet.
- **Display the RTT for each packet** and an overall summary of the average RTT and the success rate.

### How to Run

~~~
sudo python3 cs3640-ping.py -destination <destination_ip> -n <number_of_packets> -ttl <ttl_value>
~~~

- <destination_ip>: The IP address or domain name of the destination host.
- <number_of_packets>: The number of ICMP Echo requests to send.
- <ttl_value>: The Time-To-Live value for the packets.

#### Sample Output: 
~~~
destination = 8.8.8.8; icmp_seq = 0; icmp_id = 0; ttl = 100; rtt = 14.0 ms
destination = 8.8.8.8; icmp_seq = 1; icmp_id = 1; ttl = 100; rtt = 14.2 ms
destination = 8.8.8.8; icmp_seq = 2; icmp_id = 2; ttl = 100; rtt = 14.5 ms
Average rtt: 14.2 ms; 3/3 successful pings.
~~~
## Task 2: Implementing the Traceroute Program
### Description

Create a Python program `cs3640-traceroute.py` that traces the network path to a destination using ICMP Echo messages with incrementing TTL values. The program should:

Reuse functions from the Ping program.
Start with a TTL of 1 and increase it with each packet sent.
Stop when the destination is reached or the maximum number of hops is exceeded.
Display the IP address of each hop and the RTT for each hop.
### How to Run
~~~
sudo python3 cs3640-traceroute.py -destination <destination_ip> -n_hops <max_hops>
~~~

- <destination_ip>: The IP address or domain name of the destination host.
- <max_hops>: The maximum number of hops to trace.
#### Sample Output: 
~~~
destination = 8.8.8.8; hop 1 = 192.168.1.1; rtt = 0.50 ms
destination = 8.8.8.8; hop 2 = 10.0.0.1; rtt = 0.72 ms
destination = 8.8.8.8; hop 3 = 172.16.0.1; rtt = 4.51 ms
~~~
## Task 3: Implementing the Intelligence Server and Client
### Description
Implement a TCP server `cs3640-intelserver.py` that provides network intelligence services based on client requests, and a client `cs3640-intelclient.py` that communicates with this server.

#### Client Command Descriptions:
- `IPV4_ADDR(domain)`: Returns the IPv4 address of the queried domain. <br>
- `IPV6_ADDR(domain)`: Returns the IPv6 address of the queried domain.<br>
- `TLS_CERT(domain):` Returns the TLS/SSL certificate associated with the queried domain.<br>
- `HOSTING_AS(domain)`: Returns the Autonomous System (AS) that hosts the queried domain's IP.<br>
- `ORGANIZATION(domain)`: Returns the name of the organization associated with the domain's TLS certificate.<br> 

### How to Run 

#### Starting the Intelligence Server
~~~
python3 cs3640-intelserver.py
~~~
#### Using the Intelligence Client
~~~
python3 cs3640-intelclient.py <intel_server_addr> <intel_server_port> <domain> <service>
~~~ 
* <intel_server_addr>: The address of the Intelligence Server (e.g., 127.0.0.1).
* <intel_server_port>: The port on which the Intelligence Server is listening (e.g., 5555).
* <domain> : The domain to query (e.g., example.com).
* <service> : The network intelligence service to request.
- Services Available:
    - IPV4_ADDR
    - IPV6_ADDR
    - TLS_CERT
    - HOSTING_AS
    - ORGANIZATION

## Credits/Resources: 

**ChatGPT**
- Resource: [ChatGPT](https://chat.openai.com/)
- Contribution: Portions of the code were developed with the assistance of AI tools and were adapted to meet the assignment requirements. <br>

**dnspython Module**
- Resources: [dnspython Documentation](https://www.dnspython.org/)<br>
[The dns.resolver.Resolver](https://dnspython.readthedocs.io/en/latest/resolver-class.html)
- Contribution: Used for DNS resolution in the Intelligence Server. <br> 

**ipwhois Module**
- Rosurce: [ipwhois Documentation](https://pypi.org/project/ipwhois/)
- Contribution: Used for performing WHOIS lookups to retrieve AS information in the Intelligence Server.

**dpkt Module**
- Resource: [dpkt Documentation](https://dpkt.readthedocs.io/en/latest/)
- Contribution: Used for crafting and parsing network packets in the Ping and Traceroute programs.

## Contribution/Credit Reel:
**William Lucas(HawkID: wplucas)** <br>
- Task completed:
    - 1
    - 2

**Krisham Prasai (HawkID: kprasai)** <br>
- Task completed:
    - 1
    - 2

**Alan Chen (HawkID: alachen)** <br>
- Task completed:
    - Impletemented Error Handling for the scripts. 
    - Implemented get_ORGANIZATION() & get_HOSTING_AS() in `cs3640-intelserver.py`
    -  Ensuring documentation standards for this assignment (well-documented code, Readme, credit Reel).

**Vinayak Deshpande (HawkID: vdeshpande)** <br>
- Task completed:
    - 1
    - 2