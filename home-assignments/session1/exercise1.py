from __future__ import division
import json
import sys
import os.path
try:
    import yaml
except ImportError as e:
    print("{} : Please install yaml module: pip install pyyaml".format(e))


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
    ages_data = json_content["ppl_ages"]
    oldest_age = max(ages_data.values())

    bucket_data = json_content["buckets"]
    bucket_data.append(oldest_age)
    bucket_data.sort()

    dynamic_bucket_list = list(zip(bucket_data, bucket_data[1:]))
    min_bucket = min(bucket_data)
    max_bucket = max(bucket_data)
    ages_dict = ages_data

    return ages_dict, dynamic_bucket_list, min_bucket, max_bucket


def append_key_into_output(output_list, key, output_list_name):
    try:
        [output_list_name].append(key)
        output_list[str(output_list_name)] += [key]
    except Exception as e:
        print(e)


def create_yaml_based_on_bucket_ranges(ages_dict, dynamic_bucket_list, min_bucket, max_bucket, filename):
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
                        append_key_into_output(output_list, key1, out_list_name)
                    else:
                        output_list[out_list_name] = []
                        append_key_into_output(output_list, key1, out_list_name)

    with open("{}.yaml".format(filename), "w") as outfile:
        yaml.dump(output_list, outfile, allow_unicode=True)
    print(output_list)


def main(filename):
    """
    Please install yaml module before running the script
    Command: pip install pyyaml
    """
    json_content = load_json_file(filename)
    ages_dict, dynamic_bucket_list, min_bucket, max_bucket = get_ages_and_bucket_ranges(json_content)
    short_file_name = os.path.splitext(filename)[0]
    create_yaml_based_on_bucket_ranges(ages_dict, dynamic_bucket_list, min_bucket, max_bucket, short_file_name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Please add file path arg: {sys.argv[0]} <data_file_name>")
    else:
        main(sys.argv[1])
