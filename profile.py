"""3 bare metal server to test out bloom filter with DNSSEC

- 1 client 
- 1 resolver
- 1 nameserver
"""

#
# NOTE: This code was machine converted. An actual human would not
#       write code like this!
#

HARDWARE_TYPE = "c220g1"
WISC_URN = "urn:publicid:IDN+wisc.cloudlab.us+authority+cm"

# Import the Portal object.
import geni.portal as portal 
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal object,
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Node client
client_script = """
sudo apt update
sudo apt install -y dnsperf
"""

node_client = request.RawPC('client')
# node_client.hardware_type = HARDWARE_TYPE
node_client.component_manager_id = WISC_URN  # <--- Force Location: Wisconsin
node_client.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU24-64-STD'
iface0 = node_client.addInterface('client-interface', pg.IPv4Address('192.168.10.1','255.255.255.0'))

# node_client.addService(pg.Execute(shell="bash", command=client_script))

# Node resolver
resolver_script = """
# dependencies for liboqs
sudo apt update 

sudo apt install -y astyle cmake gcc ninja-build libssl-dev python3-pytest python3-pytest-xdist unzip xsltproc doxygen graphviz python3-yaml valgrind
git clone -b main https://github.com/open-quantum-safe/liboqs.git
cd liboqs

mkdir build && cd build
cmake -GNinja -DOQS_MINIMAL_BUILD="SIG_ml_dsa_44;SIG_ml_dsa_65;SIG_ml_dsa_87" ..
ninja

ninja install

cd

git clone https://github.com/HuMiTriet/unbound.git

cd unbound
./configure --enable-debug --enable-filter --enable-oqs

make 

make install

cd
"""


node_resolver = request.RawPC('resolver')
# node_resolver.hardware_type = HARDWARE_TYPE
node_resolver.component_manager_id = WISC_URN  # <--- Force Location: Wisconsin
node_resolver.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU24-64-STD'
iface1 = node_resolver.addInterface('res-interface', pg.IPv4Address('192.168.10.2','255.255.255.0'))
iface2 = node_resolver.addInterface('resolver-interface', pg.IPv4Address('192.168.20.1','255.255.255.0'))

# node_resolver.addService(pg.Execute(shell="bash", command=resolver_script))

# Node NS
ns_script = """
sudo apt update
sudo apt install -y nsd
"""


node_NS = request.RawPC('NS')
node_NS.hardware_type = HARDWARE_TYPE
node_NS.component_manager_id = WISC_URN  # <--- Force Location: Wisconsin
node_NS.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU24-64-STD'
iface3 = node_NS.addInterface('ns-interface', pg.IPv4Address('192.168.20.2','255.255.255.0'))

# node_NS.addService(pg.Execute(shell="bash", command=ns_script))

# Link client-resolver-link
link_client_resolver_link = request.LAN('client-resolver-link')
link_client_resolver_link.Site('undefined')
link_client_resolver_link.addInterface(iface1)
link_client_resolver_link.addInterface(iface0)

# Link resolver-ns-link
link_resolver_ns_link = request.LAN('resolver-ns-link')
link_resolver_ns_link.Site('undefined')
link_resolver_ns_link.addInterface(iface2)
link_resolver_ns_link.addInterface(iface3)

link_resolver_ns_link.latency = 25


# Print the generated rspec
pc.printRequestRSpec(request)
