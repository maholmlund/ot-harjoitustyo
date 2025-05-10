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
        "currency": ("€", str),
        "dbfile": ("database.db", str),
        "categories": (["ruoka", "liikenne", "liikunta", "kulttuuri", "sijoitukset"], list)
    }
    for key, (value, target_type) in default_values.items():
        if key not in data:
            data[key] = value
        elif not isinstance(data[key], target_type):
            print(f"invalid type for {key}, using default option")
            data[key] = value
    return data


CONFIG = load_config()
