from tomllib import load, TOMLDecodeError
import os


def load_config():
    data = {}
    if os.path.isfile("trackerconf.toml") and os.access("trackerconf.toml", os.R_OK):
        with open("trackerconf.toml", "rb") as f:
            try:
                data = load(f)
            except TOMLDecodeError:
                print("Error reading config file: invalid format")
                print("Using default configuration")
    else:
        print("Error reading config file: could not open file")
        print("Using default configuration")
    default_values = {
        "currency": "€",
        "dbfile": "database.db",
        "categories": ["ruoka", "liikenne", "liikunta", "kulttuuri", "sijoitukset"]
    }
    for key, value in default_values.items():
        if key not in data:
            data[key] = value
    return data


CONFIG = load_config()
