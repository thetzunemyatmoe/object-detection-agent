import requests
from pathlib import Path
import time
import trafilatura

RESOURCES = [
    {
        "title": "Official_Documentation_Ultralytics",
        "url": "https://www.ultralytics.com/glossary/object-detection#the-mechanics-of-detection",
    },
    {
        "title": "What_is_Object_Detection_IBM",
        "url": "https://www.ibm.com/think/topics/object-detection",
    },
    {
        "title": "YOLO_Object_Detection_Explained_DataCamp",
        "url": "https://www.datacamp.com/blog/yolo-object-detection-explained",
    },
    {
        "title": "Getting_Started_Object_Detection_LabelStudio",
        "url": "https://labelstud.io/blog/getting-started-with-object-detection/",
    },
]


def download_html(url, title, output_path):

    try:
        print(f"  Downloading: {title}...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        # Download the page
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Use trafilatura to extract main content
        extracted_text = trafilatura.extract(response.content)

        if extracted_text is None:
            # Fallback if trafilatura fails
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
            extracted_text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in extracted_text.splitlines())
        chunks = (phrase.strip()
                  for line in lines for phrase in line.split("  "))
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)

        # Save to file
        output_file = Path(output_path) / f"{title}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(clean_text)

        print(f"    ✅ Saved: {title}.txt ({len(clean_text)} chars)")
        time.sleep(1)
        return True

    except Exception as e:
        print(f"    ❌ Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("HTML DOWNLOADER - OFFICIAL DOCUMENTATION")
    print("=" * 70)

    output_dir = Path("data/raw/html")
    output_dir.mkdir(parents=True, exist_ok=True)

    successful = 0
    failed = 0

    print(f"\nFound {len(RESOURCES)} resources to download\n")

    for resource in RESOURCES:
        title = resource["title"]
        url = resource["url"]

        if download_html(url, title, output_dir):
            successful += 1
        else:
            failed += 1

    print("\n" + "=" * 70)
    print(f"SUMMARY: {successful} successful, {failed} failed")
    print("=" * 70)
    print(f"\nOutput saved to: {output_dir.absolute()}")
