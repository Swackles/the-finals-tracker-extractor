import json
import os
import time
from util.convert_tshark_json_to_json import convert_to_json
from util.config import save_raw_packet, get_fs_config, get_whitelisted_request_keys

config = get_fs_config()


def write_to_file(filename, data):
    path = config["base_path"] + filename

    os.makedirs(os.path.dirname(path), exist_ok=True)
    file = open(path, "w")
    file.write(data)
    file.close()


def read_from_file(filename):
    path = config["base_path"] + filename
    data = None

    if os.path.isfile(path):
        file = open(path)
        data = file.read()
        file.close()

    return data


def should_file_be_updated(filename, time_elapsed_in_minutes_between_write):
    path = config["base_path"] + filename

    if os.path.isfile(path):
        return (time.time() - os.path.getmtime(path)) / 60 > time_elapsed_in_minutes_between_write
    else:
        return True


def new_stats_file():
    return "{ \"version\": " + str(config["current_version"]) + " }"


def handle_profile_data(data):
    return {
        "embarkName": data["displayName"]["name"] + data["displayName"]["discriminator"],
        "steamName": data["thirdPartyLastSeenAccountName"]
    }


def write_player_stats_to_file(request_key, data):
    filename_stats = "stats.json"
    if save_raw_packet():
        filename_raw_json = "responses/" + request_key + "-raw.json"
        write_to_file(filename_raw_json, json.dumps(data))

    stats = read_from_file(filename_stats) or new_stats_file()
    stats = json.loads(stats)
    if stats["version"] != config.getint("current_version"):
        stats = json.loads(new_stats_file())

    if request_key == "v1-shared-profile":
        stats[request_key] = handle_profile_data(convert_to_json(data))
    else:
        stats[request_key] = convert_to_json(data)

    write_to_file(filename_stats, json.dumps(stats))

    if set(['version', *get_whitelisted_request_keys()]).issubset(set(stats.keys())):
        print("Stats file captured")
