import json
import re
from util.fs import write_player_stats_to_file, whitelisted_request_keys

header_trace_id = "x-embark-trace-id"


def analyse_packet(input):
    packet = json.loads(input)["_source"]["layers"]

    if header_trace_id in input:
        handle_embark_response(packet)


def is_whitelisted_response(key):
    return key in whitelisted_request_keys


def handle_embark_response(layers):
    key = get_request_key(layers["http"]["http.response_for.uri"])

    if is_whitelisted_response(key):
        traceid = get_http_header(layers["http"], header_trace_id)

        print("RESPONSE: ", traceid, get_path(layers["http"]["http.response_for.uri"]))
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
