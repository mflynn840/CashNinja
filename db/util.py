import json
import os
import sys

'''
Implement support for using an external JSON to store ticker data
-Resolves path for the json in development and for built program

'''
def resource_path(relative_path):
    
    '''
    Resolve a path to work during development and when packaged
    -Used to ease devlopment while supoprting building the program
    
    Args:
        reletive_path(str): relative path to the resource file
        
    Returns:
        str: the absolute path to the resource
    
    '''
    try:
        #when using pyInstaller, _MEIPass stores the temporary subpath
        base_path = sys._MEIPASS  
    #development mode
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_ticker_dict(path="./company_tickers.json"):
    
    '''
    Loads and parases a JSON file mapping tickers to company names
    
    Args:
        path (str): Path to the JSON containing the ticker data
        
    Returns:
        dict: {"tic1" : "name1",...}
    '''
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
    

