import json
from datetime import datetime, timedelta

CONFIG_FILE = "data_extraction_config.json"

def get_json_file(file_name):
    f = open(file_name)
    
    data = json.load(f)
    f.close()
    return data

def get_time_windows(minute_interval=5):
    now = datetime.now()
    minute_end = now.minute - now.minute % minute_interval
    time_end = datetime(now.year, now.month, now.day, now.hour, minute_end, 0)
    time_start = time_end - timedelta(minutes=minute_interval)
    return {
        "from": time_start.strftime("%Y-%m-%d %H:%M:%S"),
        "to" : time_end.strftime("%Y-%m-%d %H:%M:%S")
    }

def transform_file_model():
    # get configs from file
    configs:list = get_json_file(CONFIG_FILE)

    # transform file model
    position_dict = {}
    result = []
    
    while len(configs) > 0:
        config = configs.pop(0)
        parent_name = config["config"]["parent"]

        # is a root
        if parent_name == None:
            # insert properties
            config['time_window'] = get_time_windows(config["config"]["interval"])
            config['children'] = []

            # save position
            parent_position = len(result)
            position_dict[config["object"]] = [parent_position]

            # save result
            result.append(config)

        # has a parent
        elif position_dict.get(parent_name) is not None:
            # insert properties
            config['time_window'] = get_time_windows(config["config"]["interval"])
            config['children'] = []

            # move to the parent
            parents = position_dict.get(parent_name)
            sub_result = result
            for parent in parents:
                sub_result = sub_result[parent]

            # save result
            parent_position = len(sub_result["children"])
            sub_result["children"].append(config)


            # save position
            new_parents = parents.copy()
            new_parents.append('children')
            new_parents.append(parent_position)
            position_dict[config["object"]] = new_parents

        # have found the parent yet
        else:
            # save to the tail of list
            configs.append(config)

    return result



if __name__ == "__main__":
    with open("transformed_configurate.json", "w") as outfile:
        json.dump(transform_file_model(), outfile)
