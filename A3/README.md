Note: I had to call "sudo python3 network_bottleneck..." with a very low Mbps otherwise you get "*** Error: Warning: sch_htb: quantum of class 50001 is big. Consider r2q change." specifically 4 and 16 Mbps.

Had trouble with connections where h1 only connects to server_ip 0.0.0.0 or localhost. maybe a mininet or firewall problem but im not sure.

installed the iPerf bindings globally (sudo pip install <package> --break-system-packages) so dont have to use virtual environment.
