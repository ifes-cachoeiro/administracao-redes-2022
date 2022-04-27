#!/usr/bin/python
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
import time
import os

BW=1000

def run_router(router):
    name = router.name
    services = ["zebra", "ripd"]
    for srv in services:
        cmd = f"/usr/sbin/{srv} "
        cmd += f"-f /tmp/quagga/{srv}-{name}.conf -d -A 127.0.0.1 "
        cmd += f"-z /tmp/zebra-{name}.api -i /tmp/{srv}-{name}.pid "
        cmd += f"> /tmp/{srv}-{name}-router.log 2>&1"
        router.cmd(cmd)
        time.sleep(1)

def enableSwitch(switch):
    switch.cmd(f"ovs-ofctl add-flow {switch.name} \"actions=output:NORMAL\"")

def addRoute(host, route):
    if host:
        host.cmd(f"ip route add {route}")

def setIP(host, iface=None, ip=None):
    if iface and ip:
        iface = iface - 1
        host.cmd(f"ifconfig {host.name}-eth{iface} {ip} up")

def topology(remote_controller):
    "Create a network."
    net = Mininet_wifi()

    info("*** Adding stations/hosts\n")

    # Rede A
    h1A = net.addHost("h1A", ip="192.0.2.1/24")
    h2A = net.addHost("h2A", ip="192.0.2.2/24")
    # Rede B
    h1B = net.addHost("h1B", ip="203.0.113.1/24")
    h2B = net.addHost("h2B", ip="203.0.113.2/24")
    # Rede C
    h1C = net.addHost("h1C", ip="198.51.100.1/24")
    h2C = net.addHost("h2C", ip="198.51.100.2/24")
    # Rede D
    h1D = net.addHost("h1D", ip="192.168.10.1/24")
    h2D = net.addHost("h2D", ip="192.168.10.2/24")

    # Roteadores
    r1 = net.addHost("r1")
    r2 = net.addHost("r2")
    r3 = net.addHost("r3")
    r4 = net.addHost("r4")
    r5 = net.addHost("r5")
    r6 = net.addHost("r6")
    r7 = net.addHost("r7")
    r8 = net.addHost("r8")
    r9 = net.addHost("r9")
    r10 = net.addHost("r10")
    r11 = net.addHost("r11")

    info("*** Adding Switches (core)\n")

    switch1 = net.addSwitch("switch1")
    switch2 = net.addSwitch("switch2")
    switch3 = net.addSwitch("switch3")
    switch4 = net.addSwitch("switch4")

    info("*** Creating links\n")

    # Rede A
    net.addLink(h1A, switch1, bw=BW)
    net.addLink(h2A, switch1, bw=BW)
    net.addLink(r1, switch1, bw=BW)
    # Rede B
    net.addLink(h1B, switch2, bw=BW)
    net.addLink(h2B, switch2, bw=BW)
    net.addLink(r11, switch2, bw=BW)
    # Rede C
    net.addLink(h1C, switch3, bw=BW)
    net.addLink(h2C, switch3, bw=BW)
    net.addLink(r7, switch3, bw=BW)
    # Rede D
    net.addLink(h1D, switch4, bw=BW)
    net.addLink(h2D, switch4, bw=BW)
    net.addLink(r7, switch4, bw=BW)
    
    net.addLink(r1, r2, bw=BW) # r1(2), r2(1)
    net.addLink(r1, r3, bw=BW) # r1(3), r3(1)
    net.addLink(r2, r4, bw=BW) # r2(2), r4(1)
    net.addLink(r3, r4, bw=BW) # r3(2), r4(2)
    net.addLink(r4, r5, bw=BW) # r4(3), r5(1)

    info("*** Starting network\n")
    net.start()
    net.staticArp()

    info("*** Enabling switches\n")

    enableSwitch(switch1)
    enableSwitch(switch2)
    enableSwitch(switch3)
    enableSwitch(switch4)
    
    info("*** Setting addresses and routes\n")

    # Rota padrao
    addRoute(h1A, "default via 192.0.2.254")
    addRoute(h2A, "default via 192.0.2.254")
    addRoute(h1B, "default via 203.0.113.254")
    addRoute(h2B, "default via 203.0.113.254")
    addRoute(h1C, "default via 198.51.100.254")
    addRoute(h2C, "default via 198.51.100.254")
    addRoute(h1D, "default via 192.168.10.254")
    addRoute(h2D, "default via 192.168.10.254")
    # Configurar enderecos IPs
    # - R1
    setIP(r1, 1, "192.0.2.254/24")
    setIP(r1, 2, "10.10.100.1/30")
    setIP(r1, 3, "10.10.100.13/30")
    # Adicionar as rotas
    # - R1
    # - R2
    # - R3
    # - R4
    # - R5
    # - R6
    # - R7
    # - R8
    # - R9
    # - R10
    # - R11

    info("*** Running CLI\n")

    CLI(net)

    info("*** Stopping network\n")
    net.stop()
    os.system("killall -9 zebra ripd bgpd ospfd > /dev/null 2>&1")


def cleanup():
    os.system("rm -f /tmp/zebra-*.pid /tmp/ripd-*.pid /tmp/ospfd-*.pid")
    os.system("rm -f /tmp/bgpd-*.pid /tmp/*-router.log")
    os.system("rm -fr /tmp/zebra-*.api")
    os.system("mn -c >/dev/null 2>&1")
    os.system("killall -9 zebra ripd bgpd ospfd > /dev/null 2>&1")
    os.system("rm -fr /tmp/quagga")
    os.system("cp -rvf conf/ /tmp/quagga")
    os.system("chmod 777 /tmp/quagga -R")
    os.system("echo 'hostname zebra' > /etc/quagga/zebra.conf")
    os.system("chmod 777 /etc/quagga/zebra.conf")

if __name__ == "__main__":
    # cleanup()
    # os.system("systemctl start zebra.service")
    setLogLevel("info")
    remote_controller = False
    topology(remote_controller)
