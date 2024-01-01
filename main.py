from util.analyse_packet import analyse_packet
from util.tshark import *


def main():
    tshark_proc = listen_to_traffic(get_interface())
    raw_data = ""

    while True:
        line = tshark_proc.stdout.readline()
        if not line:
            break

        decoded_line = line.rstrip().decode('utf-8', errors='replace')

        # First line of output
        if decoded_line.startswith("[") or decoded_line.startswith("]"):
            continue
        # Packet starts
        elif decoded_line.startswith("  {"):
            if raw_data != "":
                analyse_packet(raw_data[:-1])
            raw_data = decoded_line
        else:
            raw_data += "\n" + decoded_line

    print(tshark_proc.communicate()[1].decode('utf-8', errors='replace'))


if __name__ == "__main__":
    main()