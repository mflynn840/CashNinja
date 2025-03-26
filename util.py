import json

def get_ticker_dict(path="./company_tickers.json"):
    try:
        with open(path, 'r') as file:
            data = json.load(file)
            ticker_dict = {}
            for k, v in data.items():
                ticker_dict[v["ticker"]] = v["title"]
                
            return ticker_dict
                      
    except FileNotFoundError:
        print("Could not find JSON")
  


