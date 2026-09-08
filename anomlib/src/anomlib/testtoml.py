import os
from os import getcwd as pwd, chdir as cd
import tomllib
from pprint import pprint


def go2script():    
    # Display current working directory
    print("PWD:", pwd())

    # Path to this script
    path = __file__

    # Got to parent directory of this script
    cd(os.path.dirname(path))

    # Display current working directory
    print("PWD:", pwd())


go2script()

CONF = "./test.toml"


def load_toml(toml=CONF):
    """Load TOML data from file"""

    with open(toml, 'rb') as f:
        toml_data = tomllib.load(f)
        return toml_data


if __name__ == "__main__":
    data = load_toml()
    pprint(data, sort_dicts=False)
