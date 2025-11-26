"""
ASID Mininet Topology Builder
-----------------------------
Creates a multi-controller SDN topology for ASID experiments.
- RYU controls domain 1 (s1-s2)
- ONOS controls domain 2 (s3-s4)
- ODL controls domain 3 (s5-s6)
Each domain runs under the same Mininet instance.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time, os

class ASIDTopo(Topo):
    def build(self):
        # RYU domain
        s1, s2 = self.addSwitch('s1'), self.addSwitch('s2')
        h1, h2 = self.addHost('h1'), self.addHost('h2')
        self.addLink(h1, s1)
        self.addLink(s2, h2)
        self.addLink(s1, s2)

        # ONOS domain
        s3, s4 = self.addSwitch('s3'), self.addSwitch('s4')
        h3, h4 = self.addHost('h3'), self.addHost('h4')
        self.addLink(h3, s3)
        self.addLink(s4, h4)
        self.addLink(s3, s4)

        # ODL domain
        s5, s6 = self.addSwitch('s5'), self.addSwitch('s6')
        h5, h6 = self.addHost('h5'), self.addHost('h6')
        self.addLink(h5, s5)
        self.addLink(s6, h6)
        self.addLink(s5, s6)

        # Inter-domain link
        self.addLink(s2, s3)
        self.addLink(s4, s5)

def run_topology():
    topo = ASIDTopo()
    net = Mininet(topo=topo, switch=OVSSwitch, controller=None)
    info("*** Adding remote controllers\n")
    ryu = net.addController('ryu', controller=RemoteController, ip='127.0.0.1', port=6633)
    onos = net.addController('onos', controller=RemoteController, ip='127.0.0.1', port=6653)
    odl = net.addController('odl', controller=RemoteController, ip='127.0.0.1', port=6635)
    net.start()

    info("*** Network running\n")
    time.sleep(3)
    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel('info')
    run_topology()
