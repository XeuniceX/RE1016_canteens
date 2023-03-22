def search_by_keyword(keywords):
    matching_stalls = matching_stalls_identifier(keywords)
# check if type is list - and & space cases
    if type(matching_stalls) == list:
        print("Food stalls found: " + str(len(matching_stalls)))
        for canteen, stall in matching_stalls:
            print(canteen + " --- " + stall)
    else:
# check if type is dictionary - or case
        for n in range(1, len(keywords.split(" or")) + 1):
            print(f'Food stalls that match {str(n)} keyword{"s" if n > 1 else ""}:')
            for canteen_stall, cnt in matching_stalls.items():
                if cnt == n:
                    print(canteen_stall[0] + " --- " + canteen_stall[1])

# returns list(and) or dictionary(or) of matching keywords
def matching_stalls_identifier(keywords):
    canteens = list(canteen_stall_keywords.keys())
    matching_stalls = []
    keyword_list = keywords.lower().split(" ")
    valid_keywords = set()

# make a set of valid keywords from dictionary given
    for canteen in canteens:
        for cuisine in canteen_stall_keywords[canteen].values():
            valid_keywords.update(set(cuisine.lower().split(', ')))

# accounting for mixed rice
    if "mixed" and "rice" in keyword_list:
        index1 = keyword_list.index("mixed")
        index2 = keyword_list.index("rice")
        keyword_list[index1:index2 + 1] = [" ".join(keyword_list[index1:index2 + 1])]

# filtering the operators out of the keyword list from input by user
    operator = " "
    if "and" in keyword_list:
        operator = "and"
        keyword_list = list(filter(lambda x: x != "and", keyword_list))
    elif "or" in keyword_list:
        operator = "or"
        keyword_list = list(filter(lambda x: x != "or", keyword_list))

# case where keywords are invalid
    if not all(keyword in valid_keywords for keyword in keyword_list):
        print("No such input, try again")
        return search_by_keyword(input("Enter type of food: "))

# return list of matching stalls with operator and
    if operator == "and":
        for canteen in canteens:
            for stall, cuisine in canteen_stall_keywords[canteen].items():
                if all(keyword in cuisine.lower() for keyword in keyword_list):
                    matching_stalls.append((canteen, stall))
        return matching_stalls

# return list of matching stalls with operator and
    elif operator == " ":
        for canteen in canteens:
            for stall, cuisine in canteen_stall_keywords[canteen].items():
                if all(keyword in cuisine.lower() for keyword in keyword_list):
                    matching_stalls.append((canteen, stall))
        return matching_stalls

# return dictionary of matching stalls with its corresponding counts
    elif operator == "or":
        for canteen in canteens:
            for stall, cuisine in canteen_stall_keywords[canteen].items():
                for keyword in keyword_list:
                    if keyword in cuisine.lower():
                        matching_stalls.append((canteen, stall))
        frequency_of_stalls = Counter(matching_stalls)
        return frequency_of_stalls
def search_by_price(keywords, max_price):
    matching_stalls_price = []
    matching_stalls = matching_stalls_identifier(keywords)
    # check if type is list - and & space cases
    if type(matching_stalls) == list:
        for canteen, stall in matching_stalls:
            # check max price against price of matching stalls
            if max_price > canteen_stall_prices[canteen][stall]:
                matching_stalls_price.append((canteen, stall, canteen_stall_prices[canteen][stall]))
        # if no such stalls, sort based on matching stalls based on keywords and give the lowest prcied on
        if len(matching_stalls_price) == 0:
            print("Food stalls found:  No food stall found within specified price range.")
            for canteen, stall in matching_stalls:
                matching_stalls_price.append((canteen, stall, canteen_stall_prices[canteen][stall]))
            matching_stalls_price.sort(key=lambda x: x[2])
            print("Recommended Food Stall with the closest price range.")
            print(matching_stalls_price[0][0] + " --- " + matching_stalls_price[0][1] + " --- " + "S$" + str(
                matching_stalls_price[0][2]))
        else:
            # print stalls that are within max price
            print("Food stalls found: " + str(len(matching_stalls_price)))
            for a, b, c in matching_stalls_price:
                print(a + " --- " + b + " --- " + "S$" + str(c))

    else:
        # check if type is dictionary - or case
        for n in range(1, len(keywords.split(" or ")) + 1):
            print(f'Food stalls that match {str(n)} keyword{"s" if n > 1 else ""}:')
            count = 0
            # check max price against price of matching stalls
            for canteen_stall, cnt in matching_stalls.items():
                if cnt == n:
                    if max_price > canteen_stall_prices[canteen_stall[0]][canteen_stall[1]]:
                        count += 1
                        print(canteen_stall[0] + " --- " + canteen_stall[1] + " --- " + "S$" + str(
                            canteen_stall_prices[canteen_stall[0]][canteen_stall[1]]))
            # make a list of matching stalls with their max prices
            if count == 0:
                matching_stalls_price.clear()
                for canteen_stall, cnt in matching_stalls.items():
                    if cnt == n:
                        matching_stalls_price.append((canteen_stall[0], canteen_stall[1],
                                                      canteen_stall_prices[canteen_stall[0]][canteen_stall[1]]))
                # if no such stalls, no such combi in the first place
                if len(matching_stalls_price) == 0:
                    print(f'No food stalls that match {str(n)} keyword{"s" if n > 1 else ""}:')
                    return main()
                else:
                    # sort the stalls based on price and give lowest priced one
                    print("No food stall found within specified price range.")
                    matching_stalls_price.sort(key=lambda x: x[2])
                    print("Recommended Food Stall with the closest price range.")
                    print(matching_stalls_price[0][0] + " --- " + matching_stalls_price[0][1] + " --- " + "S$" + str(matching_stalls_price[0][2]))


