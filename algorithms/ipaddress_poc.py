from ipaddress import IPv4Address, IPv4Network, ip_network, ip_address

def find_subnet(address, cidr):
    address_object = IPv4Address(address)
    while True:
        try:
            return IPv4Network(f'{address_object}/{cidr}')
        except ValueError:
            address_object -= 1

ip = '10.126.104.194' # Example IP address
subnet_mask = '24' # Example CIDR notation
subnet = find_subnet(ip, subnet_mask)

print(f'Returned subnet: {subnet}')
print(f'Supplied Address: {ip}')
print(f'Subnet Address: {subnet.network_address}')
print(f'Usable IPs: {subnet.network_address + 1} - {subnet.broadcast_address - 1}')
print(f'Broadcast Address: {subnet.broadcast_address}')


# Define the IP address and subnet
ip = ip_address('192.168.1.110')
network = ip_network('192.168.1.10/24', False)

print()
print(f"Reference IP is: {ip} {type(ip)}")
print(f"Reference network is: {network} {type(network)}")

# Check if the IP belongs to the subnet
if ip in network:
    print("The IP address belongs to the subnet.")
else:
    print("The IP address does not belong to the subnet.")