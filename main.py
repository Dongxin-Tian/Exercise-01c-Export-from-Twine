#!/usr/bin/env python3
import sys, os, json, re, time, random
assert sys.version_info >= (3,8), "This script requires at least Python 3.8"

first = True
canShoot = False
hp = 3

def load(l):
    f = open(os.path.join(sys.path[0], l))
    data = f.read()
    j = json.loads(data)
    return j

def find_passage(game_desc, pid):
    for p in game_desc["passages"]:
        if p["pid"] == pid:
            return p
    return {}

def format_passage(description):
    description = re.sub(r'//([^/]*)//',r'\1',description)
    description = re.sub(r"''([^']*)''",r'\1',description)
    description = re.sub(r'~~([^~]*)~~',r'\1',description)
    description = re.sub(r'\*\*([^\*]*)\*\*',r'\1',description)
    description = re.sub(r'\*([^\*]*)\*',r'\1',description)
    description = re.sub(r'\^\^([^\^]*)\^\^',r'\1',description)
    description = re.sub(r'(\[\[[^\|]*)\|([^\]]*\]\])',r'\1->\2',description)
    description = re.sub(r'\[\[([^(->)]*)->[^\]]*\]\]',r'[ \1 ]',description)
    return description

# ------------------------------------------------------

def update(current, game_desc, choice):
    global first

    if current == "":
        return current

    if choice.isnumeric():
        if int(choice) > len(current["links"]) or int(choice) == 0:
            print("\n\n---------------------\n\nYour input number is invalid to be an index number. Please try again.")
            time.sleep(1.5)
        else:
            current = find_passage(game_desc, current["links"][int(choice) - 1]["pid"])
            if current:
                return current
    else:
        for l in current["links"]:
            if choice == l["name"].lower():
                current = find_passage(game_desc, l["pid"])
                if current:
                    return current
        if first == False:
            print("\n\n---------------------\n\nI don't understand what you are asking me to do. Please try again.")
            time.sleep(1.5)
        else:
            first = False
    return current

def render(current):
    print(format_passage(current["text"]))

def get_input(current):
    choice = input("What would you like to do? (type quit to exit) ")
    choice = choice.lower()
    if choice in ["quit","q","exit"]:
        return "quit"
    return choice

# ------------------------------------------------------

def main():
    game_desc = load("adventure.json")
    current = find_passage(game_desc, game_desc["startnode"])
    choice = ""

    while choice != "quit" and current != {}:
        current = update(current, game_desc, choice)
        render(current)
        choice = get_input(current)

    print("Thanks for playing!")




if __name__ == "__main__":
    main()