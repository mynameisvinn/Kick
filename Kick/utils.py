import configparser

def fetch():
    config = configparser.RawConfigParser()
    config.read('../config.properties')
    return  dict(config.items('SECTION_NAME'))