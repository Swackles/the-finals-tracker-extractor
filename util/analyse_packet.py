import json
import re
from util.fs import write_player_stats_to_file
from util.config import get_whitelisted_request_keys, get_analyser_config, print_debug

config = get_analyser_config()

def analyse_packet(input):
    packet = json.loads(input)["_source"]["layers"]

    if config["header_trace_id"] in input:
        handle_embark_response(packet)


def is_whitelisted_response(key):
    return key in get_whitelisted_request_keys()


def handle_embark_response(layers):
    traceid = get_http_header(layers["http"], config["header_trace_id"])
    key = get_request_key(layers["http"]["http.response_for.uri"])
    print_debug("Response", traceid, key)

    if is_whitelisted_response(key):
        print_debug("Whitelisted")

        print("RESPONSE:", get_path(layers["http"]["http.response_for.uri"]))
        if layers["http"]["http.content_type"] == "application/json":
            write_player_stats_to_file(
                key,
                layers["json"]
            )
        else:
            print("DATA: ", "No JSON data")


def get_http_header(http, key):
    for header in http["http.response.line"]:
        if key in header:
            return header.split(": ")[1][:-2]

    return None


def get_request_key(url):
    return get_path(url).replace("/", "-")[1:]


def get_path(url):
    return re.search(r'^https://[a-z.-]+(/.*?)$', url).group(1)
