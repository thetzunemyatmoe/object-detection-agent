from data.raw.resource import RESOURCES
from util.download_functions import process_html, process_pdf


for index, resource in enumerate(RESOURCES):
    print(f"Downloading document [{index}]")
    if resource["format"] == "html":
        process_html(
            id=index, url=resource["url"], title=resource["title"], category=resource["category"])
    else:
        process_pdf(id=index, url=resource["url"], title=resource["title"])
