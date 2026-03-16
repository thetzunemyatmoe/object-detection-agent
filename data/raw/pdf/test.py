# Import libraries
from ftplib import parse229
import io
from PyPDF2 import PdfReader

import requests
from bs4 import BeautifulSoup

# URL from which pdfs to be downloaded
url = "https://arxiv.org/pdf/1807.05511"

# Requests URL and get response object
response = requests.get(url)

print(response.status_code)
print(response.headers['content-type'])

bytes = io.BytesIO(response.content)
reader = PdfReader(bytes)
print(len(reader.pages))


print(reader.pages[4].extract_text())


# for page in reader.pages:
#     print(page.extract_text())

print("All PDF files downloaded")
