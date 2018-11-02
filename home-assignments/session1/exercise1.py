import json
from collections import defaultdict
import operator

INPUT_JSON_PATH = "/home/hans/opsschool/opsschool3-coding/home-assignments/session1/input_file.json"
OUTPUT_DIRECTORY = "/home/hans/opsschool/opsschool3-coding/home-assignments/session1/"

def load_json_file(json_file):
    """
    :param json_file: jason file path
    :return: the content of the json file
    """
    try:
        with open(json_file, "r") as d:
            data = json.load(d)
            return data

    except Exception as e:
        print(e)


def get_ages_and_bucket_ranges(json_content):
    """
    :param json_content: json_content
    :return: list of people grouped by their ages
    """
    #  people age list
    d = json_content["ppl_ages"]
    sorted_by_value = sorted(d.items(), key=lambda kv: kv[1])
    last_age = sorted_by_value[-1]

    #  sorted bucket list
    b = json_content["buckets"]
    b.append(last_age[1])
    b = [int(x) for x in b]
    b.sort()

    dynamic_bucket_list = list(zip(b, b[1:]))
    min_bucket = b[0]
    max_bucket = b[-1]
    ages_dict = d

    return ages_dict, dynamic_bucket_list, min_bucket, max_bucket


def create_yaml_based_on_bucket_ranges(ages_dict, dynamic_bucket_list, min_bucket, max_bucket):
    """
    :return: A new yaml file with people grouped by dynamic buckets
    """

    output_list = dict()

    for key, value in dynamic_bucket_list:
        list_names = "{} - {}".format(key, value)
        output_list[list_names] = []

    for key, value in dynamic_bucket_list:
        for key1, value1 in ages_dict.items():
            if str(key1) not in str(output_list):
                if key < value1 < value:
                    list_name = (str(key) + " - " + str(value))
                    output_list[str(list_name)] += [key1]

                if value1 >= max_bucket or value1 <= min_bucket:
                    out_list_name = "out of range"
                    if out_list_name in output_list:
                        [out_list_name].append(key1)
                        output_list[str(out_list_name)] += [key1]
                    else:
                        output_list[out_list_name] = []
                        [out_list_name].append(key1)
                        output_list[str(out_list_name)] += [key1]


    with open("{}output_file.yaml".format(OUTPUT_DIRECTORY), "w") as outfile:
        json.dump(output_list, outfile)
    print(output_list)


def main():
    print("loading the json file")
    json_content = load_json_file(INPUT_JSON_PATH)
    print("Listing people by ages")
    ages_dict, dynamic_bucket_list, min_bucket, max_bucket = get_ages_and_bucket_ranges(json_content)
    create_yaml_based_on_bucket_ranges(ages_dict, dynamic_bucket_list, min_bucket, max_bucket)


if __name__ == "__main__":
    main()