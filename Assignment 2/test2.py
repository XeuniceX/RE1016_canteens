import pygame
from PIL import Image
import time
import pandas as pd
from collections import defaultdict
import re
import math

def load_stall_keywords(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    keywords = {}
    for canteen in canteens:
        keywords[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_keywords_intermediate = copy.set_index('Stall')['Keywords'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_keywords = stall_keywords_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        keywords[stall_canteen][stall] = stall_keywords

    return keywords

canteen_stall_keywords = load_stall_keywords(data_location="canteens.xlsx")



def __get_operands_operators(keywords):
    keywords_wo_space = keywords.replace(" ", "")
    operators_hashmap = {}
    AND_positions = [i.start() for i in re.finditer("AND", keywords_wo_space)]
    OR_positions = [i.start() for i in re.finditer("OR", keywords_wo_space)]
    for and_pos in AND_positions:
        operators_hashmap[and_pos] = "AND"
    for or_pos in OR_positions:
        operators_hashmap[or_pos] = "OR"

    operator_keys = list(operators_hashmap.keys())
    operator_keys.sort()

    # split into operands and operators
    operators = []

    for operator in operator_keys:
        operators.append(operators_hashmap[operator])

    temp = keywords_wo_space.replace("AND", ",")
    operands_string = temp.replace("OR", ",")
    operands = operands_string.split(",")

    return [operands, operators]

def __buildFinalKeyWordList(s):
    operands, operators = __get_operands_operators(s)
    final_list = []
    cur = [operands[0]]
    operands.pop(0)

    for i in range(len(operands)):
        if operators[i] == "AND":
            cur.append(operands[i])
        else:
            final_list.append(cur)
            cur = [operands[i]]
    final_list.append(cur)
    print(final_list)
    return final_list

def __pretty_print(matching_stalls):
    count_set = set()
    ordered_single_list = []
    count = 0
    values = matching_stalls.values()
    for v in values:
        if v in count_set:
            pass
        else:
            ordered_single_list.append(v)
            count_set.add(v)
    for c in count_set:
        print(f'Food stalls that match {c} keyword{"s" if c > 1 else ""}')
        for canteen_stall, value in matching_stalls.items():
            if c == value:
                count += 1
                print(canteen_stall[0] + " --- " + canteen_stall[1])
        print("Food stalls found: ", count)


def __and_stuff(final_list):
    canteens = list(canteen_stall_keywords.keys())
    matching_stalls = defaultdict(lambda :0)
    for li in final_list:
        for canteen in canteens:
            for stall, cuisine in canteen_stall_keywords[canteen].items():
                cuisine = cuisine.replace(" ","")
                if all(el in cuisine.lower() for el in li):
                    matching_stalls[(canteen, stall)] += 1
    __pretty_print(matching_stalls)
    return matching_stalls

def main():
    final_keyword_list = __buildFinalKeyWordList("western AND chicken")
    __and_stuff(final_keyword_list)
main()