import time
import requests
import os
from bs4 import BeautifulSoup

url = input("Enter Line url (store.line.me/stickershot/product/ ... ): ")
image_name_prefix = input("How should the images be named? Ex: 'cute' will result in images being stored as cute1.png, cute2.png, etc.: ")
image_name_prefix = "".join([c for c in image_name_prefix if c.isalpha() or c.isdigit() or c==' ']).rstrip()
print("Downloading...")

if not os.path.exists(image_name_prefix):
    os.makedirs(image_name_prefix)
webpage = requests.get(url).text
soup = BeautifulSoup(webpage, 'html.parser')
for count, span in enumerate(soup.find_all("span", class_="mdCMN09Image")):
    image_url = span["style"].split("(", 1)[1].split(";", 1)[0]
    print(image_url)
    if "." in image_url:
        file_format = image_url.rsplit(".", 1)[1]
    else:
        file_format = "png"
    with open("{}/{}{}.{}".format(image_name_prefix, image_name_prefix, str(count), file_format), 'wb') as png:
        response = requests.get(image_url, stream=True)

        if not response.ok:
            print("Failed to download {}. Response: {}".format(image_url, response))
            continue

        for block in response.iter_content(1024):
            if not block:
                break

            png.write(block)

print("Done! Stored all images in {}/ \n\nPress Enter to exit.".format(image_name_prefix))
input()