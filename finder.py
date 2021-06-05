from indeed_job_scraper import Scraper

if __name__ == '__main__':
    search_terms_input = 'turkish'
    print("input verified, input is:" + str(search_terms_input))
    sc = Scraper(search_terms_input,
                 start_invisible=True)
    sc.scrap_data()
    df = sc.df.copy()
<<<<<<< Updated upstream
    df.to_csv('deneme.csv')
=======

    # Read CV
    cv = CV(cv_url).get_cv()

    # NLP
    # Need update here... (word2vec -> similarity calculation)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", required=True)
    parser.add_argument("-c", "--cv-url", required=True)
    args = parser.parse_args()
    main(args)
>>>>>>> Stashed changes
