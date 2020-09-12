from indeed_job_scraper import Scraper

if __name__ == '__main__':
    # search_terms_input = input("Please enter a keywords separated by commas:\n")
    search_terms_input = 'turkish'
    print("input verified, input is:" + str(search_terms_input))
    sc = Scraper(search_terms_input,
                 start_invisible=True)
    sc.scrap_data()
    df = sc.df.copy()
    df.to_csv('deneme.csv')
