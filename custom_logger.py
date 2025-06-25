from termcolor import colored
from dotenv import load_dotenv
import os

load_dotenv()
FILENAME = os.getenv("FILENAME")

COLORS = {
    'success': 'green',
    'error': 'red',
    'info': 'blue',
}

PHRASES = {
    'success': 'SUCCESS',
    'error': 'ERROR',
    'info': 'INFO',
}

def log(text, phrase='info', filename=''):
    print(colored(f"{PHRASES[phrase]}: {text}", COLORS[phrase]))
    if len(filename) > 0:
        append_to_file(filename, text)

def append_to_file(filename, text):
    with open(filename, 'a') as f:
        f.write(text)