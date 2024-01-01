import json
import os
import re
from util.convert_tshark_json_to_json import convert_to_json

header_request_id = "x-embark-request-id"
header_trace_id = "x-embark-trace-id"

whitelisted_responses = [
    "/v1/discovery/roundstats",
    "/v1/discovery/roundstatsummary"
]


def analyse_packet(input):
    packet = json.loads(input)["_source"]["layers"]

    if header_request_id in input:
        handle_embark_request(packet)
    elif header_trace_id in input:
        handle_embark_response(packet)


def handle_embark_request(layers):
    print("Auth token captured")

    file = open("./token.txt", "w")
    file.write(layers["http"]["http.authorization"].replace("Bearer ", ""))
    file.close()


def is_whitelisted_response(layers):
    return get_path(layers["http"]["http.response_for.uri"]) in whitelisted_responses


def handle_embark_response(layers):
    if is_whitelisted_response(layers):
        traceid = get_http_header(layers["http"], header_trace_id)

        print("RESPONSE: ", traceid, get_path(layers["http"]["http.response_for.uri"]))
        if layers["http"]["http.content_type"] == "application/json":
            filename = "./responses/" + getRequestName(layers["http"]["http.response_for.uri"]) + "-raw.json"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            file = open(filename, "w")
            file.write(json.dumps(layers["json"]))
            file.close()

            data = convert_to_json(layers["json"])
            filename = "./responses/" + getRequestName(layers["http"]["http.response_for.uri"]) + ".json"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            file = open(filename, "w")
            file.write(json.dumps(data))
            file.close()

        else:
            print("DATA: ", "No JSON data")


def get_http_header(http, key):
    for header in http["http.response.line"]:
        if key in header:
            return header.split(": ")[1][:-2]

    return None


def getRequestName(url):
    return get_path(url).replace("/", "-")[1:]


def get_path(url):
    return re.search(r'^https://[a-z\.-]+(\/.*?)$', url).group(1)
