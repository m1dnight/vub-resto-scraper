import requests
import parser

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


def get_html(url):
    r = requests.get(URL)
    return r.text


def main():
    h = parser.parse_html(get_html(URL))

    for menu in parser.parse_menus(h):
        print(menu)


if __name__ == "__main__":
    main()
