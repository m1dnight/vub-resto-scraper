import argparse
import errno
import os

import requests

import generator_v2
import parser
import generator_v1
import json

# The VUB restaurant publishes *four menus*. A Dutch and an English one for both Etterbeek and Jette.
#
#  * Weekmenu Jette
#  * Week menu Jette
#  * Weekmenu Etterbeek
#  * Week menu Etterbeek
#
#
# Each menu has *five days*: monday to friday.
#
# Each day typically 5 has dishes. For example:
#
#  * Soup: Tomatosoup
#  * Menu 1: Mac and Cheese
#  * ...

###############################################################################
# Constants
URL = 'https://student.vub.be/en/menu-vub-student-restaurant#menu-etterbeek-nl'


###############################################################################
# Helpers
def determine_filename(menu):
    if menu.language == "en":
        if menu.location == "etterbeek":
            destination = "etterbeek.en.json"
        else:
            destination = "jette.en.json"
    else:
        if menu.location == "jette":
            destination = "jette.nl.json"
        else:
            destination = "etterbeek.nl.json"
    return destination


def write_json(filename, json_dict):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_dict, f, ensure_ascii=False, indent=2)


def get_html(url):
    r = requests.get(URL)
    return r.text


def parse_args():
    parser = argparse.ArgumentParser(description='VUB Restaurant JSON generator.',
                                     epilog="Scrapes the URL at {} for the restaurant data.".format(URL))

    parser.add_argument("--output", dest="output", action="store", required=True)
    parser.add_argument("--version", dest="version", action="store", required=False, type=int, choices=[1, 2])
    args = parser.parse_args()

    return args


def mkdir(path):
    import os
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


###############################################################################
###############################################################################
def main():
    args = parse_args()

    # Parse the HTML
    h = parser.parse_html(get_html(URL))
    menus = parser.parse_menus(h)

    # Check and if need be, create the dir.
    mkdir(args.output)

    for menu in menus:
        filename = determine_filename(menu)
        json_dict = None
        if args.version == 1:
            json_dict = generator_v1.generate_json_menu(menu)
        elif args.version == 2:
            json_dict = generator_v2.generate_json_menu(menu)

        write_json(os.path.join(args.output, filename), json_dict)


if __name__ == "__main__":
    main()
