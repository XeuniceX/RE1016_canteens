import pygame
from PIL import Image
import time
import pandas as pd
from collections import defaultdict
import re
import math

# load dataset for keyword dictionary - provided
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


# load dataset for price dictionary - provided
def load_stall_prices(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    prices = {}
    for canteen in canteens:
        prices[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_prices_intermediate = copy.set_index('Stall')['Price'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_price = stall_prices_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        prices[stall_canteen][stall] = stall_price

    return prices


# load dataset for location dictionary - provided
def load_canteen_location(data_location="canteens.xlsx"):
    # get list of canteens
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    # get dictionary of {canteen:[x,y],}
    canteen_locations = {}
    for canteen in canteens:
        copy = canteen_data.copy()
        copy.drop_duplicates(subset="Canteen", inplace=True)
        canteen_locations_intermediate = copy.set_index('Canteen')['Location'].to_dict()
    for canteen in canteens:
        canteen_locations[canteen] = [int(canteen_locations_intermediate[canteen].split(',')[0]),
                                      int(canteen_locations_intermediate[canteen].split(',')[1])]

    return canteen_locations


# get user's location with the use of PyGame - provided
def get_user_location_interface():
    # get image dimensions
    image_location = 'NTUcampus.jpg'
    pin_location = 'pin.png'
    screen_title = "NTU Map"
    image = Image.open(image_location)
    image_width_original, image_height_original = image.size
    scaled_width = int(image_width_original * 0.9)  # image's width scaled according to the screen
    scaled_height = int(image_height_original * 0.9)  # image's height scaled according to the screen
    pinIm = pygame.image.load(pin_location)
    pinIm_scaled = pygame.transform.scale(pinIm, (60, 60))
    # initialize pygame
    pygame.init()
    # set screen height and width to that of the image
    screen = pygame.display.set_mode([scaled_width, scaled_height])
    # set title of screen
    pygame.display.set_caption(screen_title)
    # read image file and rescale it to the window size
    screenIm = pygame.image.load(image_location)
    screenIm_scaled = pygame.transform.scale(screenIm, (scaled_width, scaled_height))

    # add the image over the screen object
    screen.blit(screenIm_scaled, (0, 0))
    # will update the contents of the entire display window
    pygame.display.flip()

    # loop for the whole interface remain active
    while True:
        # checking if input detected
        pygame.event.pump()
        event = pygame.event.wait()
        # closing the window
        if event.type == pygame.QUIT:
            pygame.display.quit()
            mouseX_scaled = None
            mouseY_scaled = None
            break
        # resizing the window
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            screen.blit(pygame.transform.scale(screenIm_scaled, event.dict['size']), (0, 0))
            scaled_height = event.dict['h']
            scaled_width = event.dict['w']
            pygame.display.flip()
        # getting coordinate
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get outputs of Mouseclick event handler
            (mouseX, mouseY) = pygame.mouse.get_pos()
            # paste pin on correct position
            screen.blit(pinIm_scaled, (mouseX - 25, mouseY - 45))
            pygame.display.flip()
            # return coordinates to original scale
            mouseX_scaled = int(mouseX * 1281 / scaled_width)
            mouseY_scaled = int(mouseY * 1550 / scaled_height)
            # delay to prevent message box from dropping down
            time.sleep(0.2)
            break

    pygame.quit()
    pygame.init()
    return mouseX_scaled, mouseY_scaled

# Any additional function to assist search criteria can be use
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

# make list of keywords such that a and b or c = [[a,b],c]
def buildFinalKeyWordList(s):
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
    return final_list

# print output
def __stalls_print(matching_stalls):
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
        print(f'Food stalls that match {c} set of keyword{"s" if c > 1 else ""}')
        for canteen_stall, value in matching_stalls.items():
            if c == value:
                count += 1
                print(canteen_stall[0] + " --- " + canteen_stall[1])
        print("Food stalls found: ", count)

# settle each iteration of list made (treat all as and case)
def and_stuff(final_list):
    canteens = list(canteen_stall_keywords.keys())
    matching_stalls = defaultdict(lambda :0)
    for li in final_list:
        for canteen in canteens:
            for stall, cuisine in canteen_stall_keywords[canteen].items():
                cuisine = cuisine.replace(" ","")
                if all(el in cuisine.lower() for el in li):
                    matching_stalls[(canteen, stall)] += 1
    __stalls_print(matching_stalls)

# Keyword-based Search Function - to be implemented
def search_by_keyword(keywords):
    final_keyword_list = buildFinalKeyWordList(keywords)
    and_stuff(final_keyword_list)

# Price-based Search Function - to be implemented
def search_by_price(keywords, max_price):
    final_keyword_list = buildFinalKeyWordList(keywords)
    price_and_stuff(final_keyword_list, max_price)

def price_and_stuff(final_list, max_price):
    canteens = list(canteen_stall_keywords.keys())
    matching_stalls = defaultdict(lambda :0)
    for li in final_list:
        for canteen in canteens:
            for stall, cuisine in canteen_stall_keywords[canteen].items():
                cuisine = cuisine.replace(" ","")
                if all(el in cuisine.lower() for el in li):
                    matching_stalls[(canteen, stall,canteen_stall_prices[canteen][stall])] += 1

    # convert dict into a list of lists in this format [[nh, malay, $9, 2],[ns,chinese, $7, 2]]
    price_count_list = []
    for k,v in matching_stalls.items():
        temp_li = [k[0],k[1],k[2],v]
        price_count_list.append(temp_li)
    sorted_price_count_list = sorted(price_count_list, key=lambda x:(-x[2],-x[3]))
    if len(sorted_price_count_list) == 0:
        print("No matches for keywords")
        return
    i = 0
    while i < len(sorted_price_count_list) and max_price <= sorted_price_count_list[i][2]:
        i+=1
    items_that_are_in_price_range = sorted_price_count_list[i:]
    print("Number of food stalls: ", len(items_that_are_in_price_range))
    for lis in items_that_are_in_price_range:
        print(lis[0] + " --- " + lis[1] + " --- S$" + str(lis[2]))

    if len(items_that_are_in_price_range)==0:
        print("Recommended Food Stall with the closest price range.")
        print(sorted_price_count_list[-1][0] + " --- " + sorted_price_count_list[-1][1] + " --- S$" + str(sorted_price_count_list[-1][2]))

# Location-based Search Function - to be implemented
def search_nearest_canteens(user_locations, k):
    nearest_canteen = []
    for canteen, location in canteen_locations.items():
        length_a = math.dist(user_locations[0], location)
        length_b = math.dist(user_locations[1], location)
        ave_length = (length_a + length_b) / 2
        nearest_canteen.append((canteen, ave_length, length_a, length_b))
    nearest_canteen.sort(key=lambda x: x[1])
    print(f'{str(k)} nearest canteen{"s" if k != 1  else ""} found:')
    for x in range(1, k + 1):
        print(nearest_canteen[x][0])
        print("Average distance from both users: " + str(round(nearest_canteen[x][1])) + "m")
        print("Distance from user A: " + str(round(nearest_canteen[x][1])) + "m")
        print("Distance from user B: " + str(round(nearest_canteen[x][2])) + "m")

# Main Python Program Template
# dictionary data structures
canteen_stall_keywords = load_stall_keywords("canteens.xlsx")
canteen_stall_prices = load_stall_prices("canteens.xlsx")
canteen_locations = load_canteen_location("canteens.xlsx")


# main program template - provided
def main():
    print("working program")
    loop = True

    while loop:
        print("========================")
        print("F&B Recommendation Menu")
        print("1 -- Display Data")
        print("2 -- Keyword-based Search")
        print("3 -- Price-based Search")
        print("4 -- Location-based Search")
        print("5 -- Exit Program")
        print("========================")
        option = int(input("Enter option [1-5]: "))

        if option == 1:
            # print provided dictionary data structures
            print("1 -- Display Data")
            print("Keyword Dictionary: ", canteen_stall_keywords)
            print("Price Dictionary: ", canteen_stall_prices)
            print("Location Dictionary: ", canteen_locations)
        elif option == 2:
            # keyword-based search
            print("2 -- Keyword-based Search")

            # call keyword-based search function
            keywords = input("Enter type of food: ")
            search_by_keyword(keywords)

        elif option == 3:
            # price-based search
            print("3 -- Price-based Search")

            # call price-based search function
            keywords = input("Enter type of food: ")
            max_price = float(input("Enter max price: "))
            if max_price < 0:
                print("Meal price cannot be a negative number. Please try again.")
            search_by_price(keywords, max_price)

        elif option == 4:
            # location-based search
            print("4 -- Location-based Search")

            # call PyGame function to get two users' locations
            userA_location = get_user_location_interface()
            print("User A's location (x, y): ", userA_location)
            userB_location = get_user_location_interface()
            print("User B's location (x, y): ", userB_location)
            user_locations = [userA_location, userB_location]
            k = int(input("Number of canteens: "))
            if k <= 0:
                print("Warning: k cannot be negative value. Default k = 1 is set.")
                k = 1
            # call location-based search function
            search_nearest_canteens(user_locations, k)
        elif option == 5:
            # exit the program
            print("Exiting F&B Recommendation")
            loop = False


main()
