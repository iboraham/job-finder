import Scraper





if __name__ == '__main__':
    search_terms_input = input("Please enter a keywords separated by commas:\n")
    search_terms = edit_terms(search_terms_input)

    print("input verified, input is:" + str(search_terms))
    df = scraper.scrap_data(search_terms, driver)
    print(df.head())
    sc = Scraper()
