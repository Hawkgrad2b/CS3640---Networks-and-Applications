# [CS3640-A3] Network Bottleneck Simulation with Mininet and iPerf3
**Instructor**: Rishab Nithyanand <br>
**TA**: Jack Clisham <br>
**Code Authored by**: <br>
Alan Chen (HawkID: alachen) <br>
William Lucas(HawkID: wplucas)
<br> Krisham Prasai (HawkID: kprasai)

This project simulates a network bottleneck using Mininet, generates traffic using iPerf3, and analyzes network performance. <br>
The assignment is divided into three tasks:
- **Creating a Network Topology in Mininet** (network_bottleneck.py)
- **Simulating Traffic with iPerf3** (client.py and server.py)
- **Analyzing Network Performance** (analyze-perf.py)

## Installing Mininet and iPerf3 
### Install Mininet
~~~
sudo apt-get update
sudo apt-get install mininet openvswitch-switch openvswitch-testcontroller
sudo service openvswitch-switch start
~~~
### Install iPerf3
~~~ 
sudo apt-get install iperf3 python3-pip
pip3 install iperf3
~~~

## How to Run the Scripts
### Task 1: Setting Up the Network Topology 
1. **Clear Mininet State between executions**
~~~
sudo mn -c
~~~
2. **Run network_bottleneck.py**
~~~
sudo python3 network_bottleneck.py --bw_bottleneck <bottleneck_bw> --bw_other <other_bw> --time <duration>
~~~

- Default Values:
    * bw_bottleneck: 10 Mbps
    * bw_other: 100 Mbps
    * time: 10 seconds

3. **Outputs Genearted:** 
- output-network-config.txt
- output-ifconfig-h1.txt, output-ifconfig-h2.txt, output-ifconfig-h3.txt, output-ifconfig-h4.txt
- output-ping-h1.txt, output-ping-h2.txt, output-ping-h3.txt, output-ping-h4.txt
### Task 2: Simulating Traffic with iPerf
- **Automatically Run via network_bottleneck.py**
~~~
sudo python3 network_bottleneck.py
~~~
- **Manually Running Servers and Clients**
    * Starting Servers: 
~~~
sudo python3 server.py -ip <server_ip> -port <port>
~~~
* Starting Clients:
~~~
sudo python3 client.py -ip <client_ip> -port <port> -server_ip <server_ip> -test <tcp/udp>
~~~ 
**Outputs Genearted:** 
- output-tcp-10-100.json
- output-udp-10-100.json

### Task 3: Analyzing Network Performance
1. **Run analyze-perf.py**
~~~
python3 analyze-perf.py
~~~ 
2. **Outputs Genearted:** 
- analysis.png
- observations.txt

## All Expected Outputs: 
- **Network Configuration:** output-network-config.txt
- **Host Configurations:** output-ifconfig-h1.txt to output-ifconfig-h4.txt
- **Ping Tests:** output-ping-h1.txt to output-ping-h4.txt
- **iPerf3 Test Results:**
    * TCP Test: output-tcp-10-100.json
    * UDP Test: output-udp-10-100.json
- **Analysis Outputs:**
    * Graph: analysis.png
    * Observations: observations.txt
## Credits/Resources: 
**Mininet Documentation**
- Resoruce: https://mininet.org/walkthrough/
- Contribution: Guided the setup of custom network topologies and link configurations in Mininet. <br> 

**iPerf3 Documentation**
- Resoruce: https://iperf.fr/iperf-doc.php 
- Contribution: Helped in implementing network performance tests using iPerf3 and its Python bindings. <br>

**Python Subprocess Module**
- Resoruce: https://docs.python.org/3/library/subprocess.html 
- Contribution:  Used for executing external commands and scripts within Python. <br> 

**Matplotlib Library**
- Resoruce: https://matplotlib.org/stable/index.html 
- Contribution: used for plotting throughput results in analyze-perf.py <br>
## Contribution/Credit Reel
**Collaboration and Communication:** <br>
- All members collaborated and communicated well throughout the assignment.
- Regular communcations to discuss progress, challenges, and next steps.
- Code reviews were conducted to maintain code quality and consistency.
- Team members supported each other in troubleshooting issues. <br>

**William Lucas(HawkID: wplucas)** <br>
- Task completed:
    * Implemented the Mininet topology and network configuration (network_bottleneck.py). <br> 
    * Implemented the plot_results() function using matplotlib to visualize the throughput of TCP and UDP for different bottleneck bandwidth. <br>
    * Troubleshooted & debugged issues in run_perf_tests() <br>
    * code optimization and validation

**Krisham Prasai (HawkID: kprasai)** <br>
- Task completed:
    * Implemented run_perf_test() function in network_bottleneck.py. 
    * Implemented function to ave Performace metrics to the JSON files.
    * Troubleshot issues in run_perf_tests() related to client-server communication.

**Alan Chen (HawkID: alachen)** <br>
- Task completed:
    * Implemented the iPerf3 server and client scripts (server.py and client.py).
    * Implemented main() function in analyze-perf.py using subprocess library.
    *  Troubleshot issues in run_perf_tests() related to client-server communication.
    * Ensured documentation standards for this assignment (Readme and credit Reel). <br>