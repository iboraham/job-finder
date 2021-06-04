from indeed_job_scraper import Scraper
import pandas as pd
import argparse
from cv import CV


def main(args):
    search_terms_input = str(args.search)
    cv_url = str(args.cv_url)

    # Scrap indeed.co.uk
    sc = Scraper(search_terms_input, start_invisible=True)
    sc.scrap_data()
    df = sc.df.copy()

    # Read CV
    cv = CV(cv_url)
    cv.read_cv()

    # NLP
    # Need update here... (word2vec -> similarity calculation)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", required=True)
    parser.add_argument("-c", "--cv-url", required=True)
    args = parser.parse_args()
    main(args)
