from cli.logger import *


def display_company(company):
    print_info(f"Company: {company.name}")
    print_info(f"Number of Firewalls: {len(company.fw_inventory)}")
    print_info(f"Number of Zones: {len(company.zones)}")

def display_rule(rule):
    print_info(f"Rule #{rule.number}")
    print("\t", end="")
    print_info("Source hosts:")
    for h in rule.src:
        print("\t\t", end="")
        print_info(f"{h.name} -> {h.zone}")
    print("\t", end="")
    print_info("Destination hosts:")
    for h in rule.dest:
        print("\t\t", end="")
        print_info(f"{h.name} -> {h.zone}")
    print("\t", end="")
    print_info(f"Servics: {rule.services}")
    print("\t", end="")
    print_info(f"Status: {rule.status}")

def display_firewall(fw):
    # summary display without detailing every rule
    print_info(f"Firewall: {fw.name}")
    print("\t", end="")
    print_info(f"Firewall vendor: {fw.vendor}")
    print("\t", end="")
    print_info(f"Firewall IP address: {fw.address}")
    print("\t", end="")
    print_info(f"Number of interfaces: {len(fw.interfaces)}")
    for i in fw.interfaces:
        print("\t\t", end="")
        print_info(f"Interface: {i['name']} => {i['address']}")
    print("\t", end="")
    print_info(f"Number of hosts: {len(fw.hosts)}")
    print("\t", end="")
    print_info(f"Number of groups: {len(fw.groups)}")
    print("\t", end="")
    print_info(f"Number of rules: {len(fw.rules)}")

def display_fw_rules(fw):
    # more detailed with all rules and their status printed
    print(f"\n[+] Firewall: {fw.name}")
    for rule in fw.rules:
        display_rule(rule)

def display_host(host):
    print(f"[+] Host: {host.name}")