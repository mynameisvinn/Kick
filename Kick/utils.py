import configparser
from dotenv import load_dotenv, find_dotenv
import os

def fetch(field):
    """read data from config file.

    config file is saved in home directory as .kick.ini
    """
    location = os.getcwd()

    # point to home directory
    os.chdir(os.path.expanduser("~"))  # change to home dir https://python-forum.io/Thread-change-to-home-directory
    
    # get path to home and then find config file
    path = os.getcwd() + "/kick.ini"
    
    # read data
    config = configparser.ConfigParser()
    config.read(path)

    # return to original location
    os.chdir(location)
    
    return config['DEFAULT'][field]