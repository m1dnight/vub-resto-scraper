import requests
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

# Constants
URL = 'https://student.vub.be/en/menu-vub-student-restaurant#menu-etterbeek-nl'


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


def main():
    # Get the HTML and parse it.
    h = parser.parse_html(get_html(URL))
    menus = parser.parse_menus(h)

    # Print out the menus.
    for menu in menus:
        print(menu)

    # Write the menus to a file.
    for menu in menus:
        filename = determine_filename(menu)
        json_dict = generator_v1.generate_json_menu(menu)
        write_json(filename, json_dict)


if __name__ == "__main__":
    main()
