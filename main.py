# Press the green button i  n the gutter to run the script.
import argparse
import errno
import json
import os

from Generator import Generator
from Scraper import Scraper


def parse_args():
    parser = argparse.ArgumentParser(description='VUB Restaurant JSON generator.',
                                     epilog="Scrapes the VUB website for the restaurant data.")

    parser.add_argument("--output", dest="output", action="store", required=True)
    parser.add_argument("-t", "--history", dest="history", action="store_true", help="Keep old values")
    parser.add_argument("--version", dest="version", action="store", required=False, type=int, choices=[1, 2])
    args = parser.parse_args()

    args.history_path = os.path.join(args.output, "history")
    return args


def read_file_to_json(file):
    if not os.path.exists(file):
        return {}
    else:
        with open(file) as f:
            content = json.load(f)
            return content


def history(directory, history):
    for filename in ["jette.en.json", "jette.nl.json", "etterbeek.en.json", "etterbeek.nl.json"]:
        latest_path = os.path.join(directory, filename)
        history_path = os.path.join(history, filename)

        latest_content = read_file_to_json(latest_path)
        history_content = read_file_to_json(history_path)

        for day in latest_content:
            key = day["date"]
            val = day["menus"]
            history_content[key] = val

        write_json(history_content, history_path)


def ensure_directories(args):
    mkdir(args.output)
    if args.history:
        mkdir(args.history_path)


def write_json(json_dict, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_dict, f, ensure_ascii=False, indent=2)


def mkdir(path):
    import os
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def main():
    args = parse_args()
    ensure_directories(args)

    scraper = Scraper()

    jette_nl = Generator.generate(scraper.get_restaurant(Scraper.jette_nl))
    write_json(jette_nl, os.path.join(args.output, "jette.nl.json"))
    
    jette_en = Generator.generate(scraper.get_restaurant(Scraper.jette_en))
    write_json(jette_en, os.path.join(args.output, "jette.en.json"))
    
    etterbeek_nl = Generator.generate(scraper.get_restaurant(Scraper.etterbeek_nl))
    write_json(etterbeek_nl, os.path.join(args.output, "etterbeek.nl.json"))

    etterbeek_en = Generator.generate(scraper.get_restaurant(Scraper.etterbeek_en))
    write_json(etterbeek_en, os.path.join(args.output, "etterbeek.en.json"))

    if args.history:
        if args.version == 1:
            history(args.output, args.history_path)
        elif args.version == 2:
            history(args.output, args.history_path)


if __name__ == "__main__":
    main()
