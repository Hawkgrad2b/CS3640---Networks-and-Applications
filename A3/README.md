Note: I had to call "sudo python3 network_bottleneck..." with a very low Mbps otherwise you get "*** Error: Warning: sch_htb: quantum of class 50001 is big. Consider r2q change." specifically 4 and 16 Mbps.

Had trouble with connections where h1 only connects to server_ip 0.0.0.0 or localhost. maybe a mininet or firewall problem but im not sure. Maybe this piazza thread answers it but ive been trying for too long and just saw this and im done for now: "My group figured it out. In run_perf_tests(), we recreated the topology object and got each host (eg. h3 = net.get("h3")). Then, we ran server.py and client.py on certain hosts (eg. tcp_server = h3.cmd('sudo python3 server.py -ip=10.0.0.3 -port=5201 &'))."

installed the iPerf bindings globally (sudo pip install <package> --break-system-packages) so dont have to use virtual environment.
