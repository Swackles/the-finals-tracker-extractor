import subprocess
import os
from util.config import get_tshark_config, save_tshark_config

config = get_tshark_config()

def get_interface():
    print(config["path"])
    interface = config["interface"]
    if interface == "":
        process = subprocess.Popen([config["path"], "-D"], shell=True)
        process.communicate()

        interface = input("\n\nSelect interface number: ")
        save = input("Would you like to use this interface next time? (y/n): ")
        if (save == "y"):
            config["interface"] = interface
            save_tshark_config(config)

    return interface


def listen_to_traffic(interface):
    call = [
        config["path"],
        "-i", interface,
        "-o", "ssl.keylog_file:" + os.getenv('SSLKEYLOGFILE'),
        "-T", "json",
        "--no-duplicate-keys",
        "-Vl",
        "-Y", "http && (http contains \"x-embark-request-id\" || http contains \"x-embark-trace-id\")"
    ]

    p = subprocess.Popen(
        call,
        bufsize=0,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE
    )

    print("Started capture on interface", interface)

    return p
