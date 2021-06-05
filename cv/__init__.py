import PyPDF2
import urllib


class CV:
    def __init__(self, url):
        self.url = url
        pdfFileObj = urllib.request.urlopen(self.url)
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pageObj = pdfReader.getPage(0)
        self.text = pageObj.extractText()
        pdfFileObj.close()

    def get_cv(self):
        return self.text
