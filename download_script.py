from data.raw.resource import RESOURCES
from util.download_functions import process_html, process_pdf, save_data


data = []

for index, resource in enumerate(RESOURCES):
    print(f"Downloading document [{index}]")
    url = url = resource["url"]
    content = ""
    if resource["format"] == "html":
        content = process_html(url)
    else:
        content = process_pdf(url)

    if len(content) != 0:
        data.append(
            {
                "id": index,
                "source": resource["title"],
                "url": url,
                "category": resource["category"],
                "content": content
            }
        )

print(data[0])
save_data(data)
