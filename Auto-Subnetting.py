#!/usr/bin/python3

def mask_to_binary(mask):
    mask_byte_list = mask.split(".")
    mask_in_binary = []
    for byte_nr in range(len(mask_byte_list)):
        byte = bin(int(mask_byte_list[byte_nr]))
        mask_in_binary.append(str(byte)[2:])
    return mask_in_binary

def concat_list(listy):
    concatenated_list = ".".join(listy)
    return concatenated_list

def binary_to_slash(binary_mask):
    slash_number = 0
    for byte in range(len(binary_mask)):
        current_byte = binary_mask[byte]
        for bit in range(len(current_byte)):
            if current_byte[bit:bit +1] == "1":
                slash_number += 1
    slash = "/" + str(slash_number)
    return slash

def hosts_to_mask(max_hosts):
    mask_fullbyte_list = [255,255,255,255]
    byte_nr = 0
    max_hosts += 1
    while max_hosts > 0:
        if mask_fullbyte_list[byte_nr] >= max_hosts:
            mask_fullbyte_list[byte_nr] -= max_hosts
            max_hosts -= max_hosts
        else:
            while mask_fullbyte_list[byte_nr] == 0:
                byte_nr += 1
            mask_fullbyte_list[byte_nr] -= 1
            max_hosts -= 255**byte_nr+1
    for byte in range(len(mask_fullbyte_list)):
        mask_fullbyte_list[byte] = str(mask_fullbyte_list[byte])
    mask_fullbyte_list.reverse()
    mask = concat_list(mask_fullbyte_list)         
    return mask

def mask_and_IP_to_broadcast(mask, IP):
    mask_byte_list = mask.split(".")
    IP_byte_list = IP.split(".")
    broadcast_byte_list = []
    for byte_nr in range(len(mask_byte_list)):
        broadcast_byte_list.append(str(int(IP_byte_list[byte_nr]) + 255 - int(mask_byte_list[byte_nr])))
    broadcast = concat_list(broadcast_byte_list)
    return broadcast

choice = input("Enter (1) for getting info based off subnet mask\nEnter (anything else) for getting info based off Network IP and Subnet CIDR (Broadcast IP retriveable)\n")

if choice == "1":
    Mask = input("\nInput Subnet Mask (Ex. 255.255.255.0): ")

    mask_in_binary = mask_to_binary(Mask)
    slash = binary_to_slash(mask_in_binary)
    hosts_exponent = 32 - int(slash[1:])
    max_hosts = 2 ** hosts_exponent - 2

    print("----------------------------------")
    print("Here is the subnet mask: " + Mask)
    print("Here is the mask in binary: " + concat_list(mask_in_binary))
    print("Here is the subnet's CIDR: " + slash)
    print("Here is the max number of hosts: " + str(max_hosts))
    print("----------------------------------")

else:
    IP_and_CIDR = input("\nInput Network IP and CIDR (Ex. 192.168.1.0/24): ")
    
    slash = IP_and_CIDR[IP_and_CIDR.index("/"):]
    hosts_exponent = 32 - int(slash[1:])
    max_hosts = 2 ** hosts_exponent - 2
    Mask = hosts_to_mask(max_hosts)
    mask_in_binary = mask_to_binary(Mask)
    broadcast = mask_and_IP_to_broadcast(Mask, IP_and_CIDR[:IP_and_CIDR.index("/")])

    print("----------------------------------")
    print("Here is the subnet mask: " + Mask)
    print("Here is the mask in binary: " + concat_list(mask_in_binary))
    print("Here is the subnet's CIDR: " + slash)
    print("Here is the max number of hosts: " + str(max_hosts))
    print("Here is the Broadcast IP: " + broadcast)
    print("----------------------------------")
