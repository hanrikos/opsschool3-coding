import json
from collections import defaultdict


INPUT_JSON_PATH = "/home/hans/opsschool/opsschool3-coding/home-assignments/session1/input_file.json"
OUTPUT_DIRECTORY = "/home/hans/opsschool/opsschool3-coding/home-assignments/session1/"

def load_json_file(json_file):
    """
    :param json_file: jason file path
    :return: the content of the json file
    """
    with open(json_file, "r") as d:
        data = json.load(d)
        return data


def group_by_age(json_content):
    """
    :param json_content: json_content
    :return: list of people grouped by their ages
    """
    d = json_content["ppl_ages"]

    range_one = []  # 11 to 20
    range_two = []  # 20 to 25
    range_three = []  # 25 to 40
    range_four = []  # 40 to 102
    out_of_ranges = []  # out of range

    for key, value in d.items():
        if 11 < value < 20:
            range_one.append(key)
        if 20 < value < 25:
            range_two.append(key)
        if 25 < value < 40:
            range_three.append(key)
        if 40 < value < 102:
            range_four.append(key)
        else:
            out_of_ranges.append(key)

    return range_one, range_two, range_three, range_four, out_of_ranges


def append_multiple_jsons(range_one, range_two, range_three, range_four, out_of_ranges):
    """
    :return: A new json file with people grouped by their ages
    """
    output_list = dict()
    output_list["11 to 20"] = range_one
    output_list["20 to 25"] = range_two
    output_list["25 to 40"] = range_three
    output_list["40 to 102"] = range_four
    output_list["Out of range"] = out_of_ranges

    with open("{}output_file.yaml".format(OUTPUT_DIRECTORY), "w") as outfile:
        json.dump(output_list, outfile)
    print(output_list)


def main():
    print("loading the json file")
    json_content = load_json_file(INPUT_JSON_PATH)
    print("Listing people by ages")
    range_one, range_two, range_three, range_four, out_of_ranges = group_by_age(json_content)
    print(range_one, range_two, range_three, range_four, out_of_ranges)
    print("Creating new Json")
    append_multiple_jsons(range_one, range_two, range_three, range_four, out_of_ranges)


if __name__ == "__main__":
    main()