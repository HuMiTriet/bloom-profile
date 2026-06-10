from mergexp import *

net = Network("bloom-dnssec", routing == static, addressing == ipv4)

client = net.node(
    "client",
    metal == False,
    proc.cores == 8,
    memory.capacity == gb(16),
    image == "client",
)

attacker = net.node(
    "attacker",
    metal == False,
    proc.cores == 24,
    memory.capacity == gb(32),
    image == "attacker",
)

resolver = net.node(
    "resolver",
    metal == False,
    proc.cores == 16,
    memory.capacity == gb(32),
    image == "resolver",
)

pqcns = net.node(
    "pqcns",
    metal == False,
    proc.cores == 80,
    memory.capacity == gb(192),
    disk.capacity == gb(200),
)

# client, attacker --- resolver --- pqcns


client_resolver_link = net.connect(
    [client, resolver],
    latency == ms(1),
    capacity == mbps(1000),
    layer == 3,
)

client_resolver_link.properties["tags"] = "c_r"

attacker_resolver_link = net.connect(
    [attacker, resolver],
    latency == ms(1),
    capacity == mbps(2000),
    layer == 3,
)

attacker_resolver_link.properties["tags"] = "a_r"

client_resolver_link[client].socket.addrs = ip4("192.168.10.1/24")
client_resolver_link[resolver].socket.addrs = ip4("192.168.10.2/24")

attacker_resolver_link[attacker].socket.addrs = ip4("192.168.11.1/24")
attacker_resolver_link[resolver].socket.addrs = ip4("192.168.11.2/24")


resolver_pqcns_link = net.connect(
    [resolver, pqcns],
    latency == ms(25),
    capacity == mbps(1000),
    layer == 3,
)

resolver_pqcns_link.properties["tags"] = "r_n"

resolver_pqcns_link[resolver].socket.addrs = ip4("192.168.20.1/24")
resolver_pqcns_link[pqcns].socket.addrs = ip4("192.168.20.2/24")


experiment(net)
