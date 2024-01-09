import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')


def save_config():
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def get_tshark_config():
    return config["tshark"]


def save_tshark_config(tshark_config):
    config["tshark"] = tshark_config
    save_config()


def get_fs_config():
    return config["fs"]


def get_analyser_config():
    return config["analyser"]


def get_whitelisted_request_keys():
    return json.loads(get_analyser_config()["whitelisted_request_keys"])


def save_raw_packet():
    return config.getboolean("debug", "save_raw")


def print_debug(*msg):
    if config.getboolean("debug", "log"):
        print(*msg)
