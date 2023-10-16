# =====================================
# Imports
# =====================================

from rym_parser import RymParser
from app import run_app
import argparse

# =====================================
# Constants
# =====================================

HELP_MESSAGE = """you must first scrape data (with the --scrape option), and you can present the data you scraped with \
the --display option"""

# =====================================
# Functions
# =====================================

def main():
    parser = argparse.ArgumentParser(description='Scrape and save your RYM collection')

    action = parser.add_mutually_exclusive_group()
    action.add_argument("-s", "--scrape", action="store_true", help="scraping the data")
    action.add_argument("-d", "--display", action="store_true", help="displaying and filtering the data")

    scrape_group = parser.add_argument_group('scraping')
    scrape_group.add_argument("-u", "--username", action="store", help="username to scrape data from")
    scrape_group.add_argument("-o", "--output_path", action="store", default="data", help="output path")
    scrape_group.add_argument("-sr", "--start_rating", action="store", default=0.5, type=float,
                                help="rating to start scrape at")
    scrape_group.add_argument("-er", "--end_rating", action="store", default=5.0, type=float,
                                help="rating to end scrape at")
    scrape_group.add_argument("-r", "--recovery_mode", default=False, action="store_true", 
                        help="use this to continue where you left off if scraping crashed midway (after link generation)")

    display_group = parser.add_argument_group('displaying')
    display_group.add_argument("-dp", "--data_path", action="store", default="data/release_data.json", 
                               help="path to release.json file")
    display_group.add_argument("-p", "--port", action="store", default=5000, type=int, help="port to run server from")

    args = parser.parse_args()
    assert(args.start_rating <= args.end_rating), "start_rating should be lower than or equal to end_rating"

    if args.scrape:
        assert(args.username != None), "Please must enter a username to scrape from (--username)"
        scraper(args.username, args.output_path, args.start_rating, args.end_rating, args.recovery_mode)
    elif args.display:
        display(args.data_path, args.port)
    else:
        print(HELP_MESSAGE)


def scraper(username, output_path, start_rating, end_rating, recovery_mode):
    with RymParser(username, start_rating=start_rating, end_rating=end_rating, output_path=output_path) as rym_parser:
        if recovery_mode:
            rym_parser.recover()
        else:
            rym_parser.scrape_and_save_collection_releases_url()
            rym_parser.scrape_and_save_release_data()


def display(data_path, port):
    run_app(data_path, port=port)


if __name__ == '__main__':
    main()

