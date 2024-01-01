import subprocess
import os

tshark_path = "C:\Program Files\Wireshark\\tshark.exe"

def get_interface():
    process = subprocess.Popen([tshark_path, "-D"], shell=True)
    process.communicate()

    interface = input("\n\nSelect interface number: ")
    return interface


def listen_to_traffic(interface):
    call = [
        tshark_path,
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