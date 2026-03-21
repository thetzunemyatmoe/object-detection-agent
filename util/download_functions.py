from numpy import source

from PyPDF2 import PdfReader
import trafilatura
import json

from bs4 import BeautifulSoup
import requests
import io


def process_pdf(url):
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
        content = '\n'.join(line for line in lines if line)

        return content
    except Exception as e:
        print(f"Error: {str(e)}")
        return ""


def process_html(url):
    try:

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        # Download the page
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Use trafilatura to extract main content
        extracted_text = trafilatura.extract(response.content)

        if extracted_text is None:
            # Fallback if trafilatura fails
            soup = BeautifulSoup(response.content, 'html.parser')

            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
            extracted_text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in extracted_text.splitlines())
        chunks = (phrase.strip()
                  for line in lines for phrase in line.split("  "))
        content = '\n'.join(chunk for chunk in chunks if chunk)

        return content

    except Exception as e:
        print(f"Error: {str(e)}")
        return ""


def save_data(data):

    with open("data/processed/data.json", "w") as f:
        json.dump(data, f, indent=2)
