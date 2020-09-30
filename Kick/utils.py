from configparser import SafeConfigParser
import os

def fetch(section, field):
    print(os.getcwd())
    parser = SafeConfigParser()
    parser.read('/config.ini')
    return parser.get(section, field)