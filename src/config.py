from tomllib import load, TOMLDecodeError


def load_config():
    data = {}
    try:
        f = open("trackerconf.toml", "rb")
        data = load(f)
    except OSError:
        print("Error reading config file: could not open file")
        print("Using default configuration")
    except TOMLDecodeError:
        print("Error reading config file: invalid format")
        print("Using default configuration")
    default_values = {
        "currency": "€",
        "dbfile": "database.db",
        "categories": ["ruoka", "liikenne", "liikunta", "kulttuuri", "sijoitukset"]
    }
    for key in default_values.keys():
        if key not in data:
            data[key] = default_values[key]
    return data


CONFIG = load_config()
