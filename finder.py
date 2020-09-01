from indeed_job_scraper import Scraper

if __name__ == '__main__':
    search_terms_input = input("Please enter a keywords separated by commas:\n")

    print("input verified, input is:" + str(search_terms_input))
    sc = Scraper(search_terms_input, start_invisible=False)
    sc.scrap_data()
    df = sc.df.copy()
    print(df.head())
