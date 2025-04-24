import json
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # Set by PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_ticker_dict(path="./company_tickers.json"):
    path = resource_path(path)
    try:
        with open(path, 'r') as file:
            data = json.load(file)
            ticker_dict = {}
            for k, v in data.items():
                ticker_dict[v["ticker"]] = v["title"]
                
            return ticker_dict

    except FileNotFoundError:
        print("Could not find JSON")
    

