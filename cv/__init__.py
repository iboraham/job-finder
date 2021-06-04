import PyPDF2
import urllib


class CV:
    def __init__(self, url):
        self.url = url

    def read_cv(self):

        # creating a pdf file object
        pdfFileObj = urllib.request.urlopen(self.url)

        # creating a pdf reader object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        # creating a page object
        pageObj = pdfReader.getPage(0)

        # extracting text from page
        self.text = pageObj.extractText()

        # closing the pdf file object
        pdfFileObj.close()
