#!/bin/python3 -W ignore
from scapy.all import *
import random
import re
import argparse
import csv

src = '192.168.0.101'
sport = random.randrange(49152, 65535)
dst = '10.0.0.101'
dport = 80
scenario = []
file_out = "out.pcap"


def tcp_establish(src=src, sport=sport, dst=dst, dport=dport):
    SYN = IP(src=src, dst=dst)/TCP(sport=sport, dport=dport,
             flags='S', seq=random.randint(10000, 500000))
    SYNACK = IP(src=dst, dst=src)/TCP(sport=dport, dport=sport,
                flags='SA', seq=random.randint(10000, 500000), ack=SYN[TCP].seq+1)
    ACK = IP(src=src, dst=dst)/TCP(sport=sport, dport=dport,
             flags='A', seq=SYNACK[TCP].ack, ack=SYNACK[TCP].seq+1)
    return [SYN, SYNACK, ACK], [SYN, ACK], [SYNACK]


def http_request(src=src, sport=sport, dst=dst, dport=dport, pcap=[], client=[], server=[], request_string=""):
    seq = pcap[len(pcap)-1][TCP].seq
    ack = pcap[len(pcap)-1][TCP].ack
    if pcap[len(pcap)-1] == server[len(server)-1]:
        seq = server[len(server)-1][tcp].ack
        ack = server[len(server)-1][tcp].seq + 1
    http_client = IP(src=src, dst=dst)/TCP(sport=sport,
                     dport=dport, flags='PA', seq=seq, ack=ack)/request_string
    pcap.append(http_client)
    client.append(http_client)
    ack_server = IP(src=dst, dst=src)/TCP(sport=dport, dport=sport, flags='A', seq=ack, ack=seq+len(request_string))
    pcap.append(ack_server)
    server.append(ack_server)

def http_response(src = src, sport = sport, dst = dst, dport = dport, pcap = [], client = [], server = [], response_string = ""):
    seq=pcap[len(pcap)-1][TCP].seq
    ack=pcap[len(pcap)-1][TCP].ack
    if pcap[len(pcap)-1] == client[len(client)-1]:
        seq=server[len(client)-1][tcp].ack
        ack=server[len(client)-1][tcp].seq + 1
    http_server=IP(src = src, dst = dst)/TCP(sport = sport,
                   dport = dport, flags = 'PA', seq = seq, ack = ack)/response_string
    pcap.append(http_server)
    server.append(http_server)
    ack_client=IP(src = dst, dst = src)/TCP(sport = dport, dport = sport, flags = 'A', seq = ack, ack = seq+len(response_string))
    pcap.append(ack_client)
    server.append(ack_client)

def gen_pcap(src=src, sport=sport, dst=dst, dport=dport, scenario=scenario, file_out=file_out):
    pcap, client, server=tcp_establish()
    for record in scenario:
        if record["type"] == "req":
            http_request(src=src, sport=sport, dst=dst, dport=dport, pcap=pcap,
                         client=client, server=server, request_string=record["content"])
        if record["type"] == "res":
            http_response(src=dst, sport=dport, dst=src, dport=sport, pcap=pcap,
                          client=client, server=server, response_string=record["content"])
    wrpcap(file_out, pcap)

def csv2dict(file_in=""):
    with open(file_in, mode='r') as file_obj:
        reader_obj=csv.reader(file_obj)
        for row in reader_obj:
            scenario.append({"type": row[0], "content": re.sub(
                '\n', '\r\n', row[1])+'\r\n\r\n'})

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description='Process some integers.')
    parser=argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='CSV scenario input file')
    parser.add_argument(
        '-o', '--output', help='PCAP output file, default is out.pcap')
    parser.add_argument(
        '--src', help='Client IP address, default value is 192.168.0.101')
    parser.add_argument(
        '--dst', help='Server IP address, default value is 10.0.0.101')
    parser.add_argument(
        '--sport', help='Client port number, default value is 49152-65535(random)')
    parser.add_argument(
        '--dport', help='Server port number, default value is 80')
    args=parser.parse_args()
    if args.input:
        csv2dict(args.input)
    if args.output:
        file_out=args.output
    if args.src:
        src=args.src
    if args.dst:
        dst=args.dst
    if args.sport:
        sport=args.sport
    if args.dport:
        dport=args.sport
    gen_pcap(src=src, sport=sport, dst=dst, dport=dport,
             scenario=scenario, file_out=file_out)
