from dotenv import load_dotenv, find_dotenv
import os

def fetch(field):
    load_dotenv(find_dotenv())
    return os.getenv(field)