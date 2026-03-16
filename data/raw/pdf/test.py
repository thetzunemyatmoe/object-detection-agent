from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import requests
import io


url = "https://openaccess.thecvf.com/content_CVPR_2020/papers/Tan_EfficientDet_Scalable_and_Efficient_Object_Detection_CVPR_2020_paper.pdf"


response = requests.get(url)
bytes = io.BytesIO(response.content)
reader = PdfReader(bytes)
s = ""
for page in reader.pages:
    s += page.extract_text()

# Remove text before Abstract
keywords = ['Abstract', 'ABSTRACT']
for keyword in keywords:
    if keyword in s:
        s = s.split(keyword)[1]

# Remove Citations
keywords = ['References', 'REFERENCES', 'Bibliography', 'BIBLIOGRAPHY']
for keyword in keywords:
    if keyword in s:
        s = s.split(keyword)[0]
        break

# Remove Acknowledgement
keywords = ['Acknowledgement', 'ACKNOWLEDGEMENT']
for keyword in keywords:
    if keyword in s:
        s = s.split(keyword)[0]

# Clean whitespace
lines = (line.strip() for line in s.splitlines())
text = '\n'.join(line for line in lines if line)

# Save to file
with open("file.txt", "w", encoding="utf-8") as f:
    f.write(text)
