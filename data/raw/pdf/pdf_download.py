from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import requests
import io
from resources import RESOURCES


def process_pdf(url, title):
    try:
        response = requests.get(url)
        byte_steam = io.BytesIO(response.content)
        reader = PdfReader(byte_steam)
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
        with open("folder/" + title + ".txt", "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def main():

    for item in RESOURCES:
        process_pdf(item["url"], item["title"])


if __name__ == "__main__":
    main()
