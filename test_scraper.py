import unittest
import indeed_job_scraper


class TestScraper(unittest.TestCase):
    """Test the scraper class"""

    def test_edit_terms(self):
        terms = 'Machine Learning, Data Scientist'
        result = indeed_job_scraper._edit_terms(terms)
        self.assertEqual(result, ['Machine+Learning', 'Data+Scientist'])


if __name__ == '__main__':
    unittest.main()
