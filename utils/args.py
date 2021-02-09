import getopt, sys
import json

# Options
options = "f:"
 
# Long options
long_options = ["config=", "cash=", "symbol="]

def get_config_from_args():
    overrides = {}
    config="example"
    if len(sys.argv) == 1 :
        print("using default example config file")
    else:
        overrides = get_cmd_line_overrides(sys.argv[1:])
    
    if overrides["config"]:
         print(f'using custom config file: {overrides["config"]}')
         config = overrides["config"]

    with open(f"algo_trading/configs/{config}.json") as json_data_file:
        data = json.load(json_data_file)

    for key in data:
        if key in overrides:
            data[key] = overrides[key]

    return data

def get_cmd_line_overrides(argumentList):
    arguments, values = getopt.getopt(argumentList, options, long_options)

    overrides = {}

    for arg, value in arguments:
        if arg in ("-f", "--config"):
            overrides['config'] = value
        elif arg == '--cash':
            overrides['cash'] = float(value)
        elif arg == '--symbol':
            overrides['symbol'] = value
    
    return overrides