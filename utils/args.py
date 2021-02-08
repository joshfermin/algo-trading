import sys
import json

def get_config_from_args():
    config = "example"
    if len(sys.argv) == 1 :
        print("using default example config file")
    else:
        print(f"using custom config file: {sys.argv[1]}")
        config = sys.argv[1]
        
    with open(f"algo_trading/configs/{config}.json") as json_data_file:
        data = json.load(json_data_file)
    return data
        