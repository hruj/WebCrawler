import io
import os
import pprint
import hashlib
import requests
from PIL import Image
from bs4 import BeautifulSoup


class Scrape_info:
    res = requests.get('https://www.imdb.com/list/ls068010962/')
    soup = BeautifulSoup(res.text, 'html.parser')

    image_links = []
    for img in soup.find_all('img'):
        image_links.append(img.get('src'))
    pprint.pprint(image_links)

    Names = []
    for img in soup.find_all('img'):
        Names.append(img.get('alt'))
    pprint.pprint(Names)

    infos = soup.find_all('p', class_=False)
    final_info = []

    for info in infos:
        info = info.get_text()
        info = info.rstrip('\n')
        # print(info)
        final_info.append(info)

    final_info = final_info[1:]
    pprint.pprint(final_info)

    bollywood_dictionary = dict()
    bollywood_dictionary["Names"] = Names
    bollywood_dictionary["Images"] = image_links
    bollywood_dictionary["Info"] = final_info
    pprint.pprint(bollywood_dictionary)
    image_save = []
    for img in image_links:
        image_content = requests.get(img).content
        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')

            file_path = os.path.join('C:\\Users\\Hrushit\\OneDrive\\Desktop\\Web Scraping\\IMDb- Bollywood '
                                     'Celebrities\\Images',
                                     hashlib.sha1(image_content).hexdigest()[:10] + ".jpg")
            image_save.append(file_path)
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=85)
            # pprint.pprint(image_save)
            print(f"SUCCESS - saved {img} - as {image_save}")
        except Exception as e:
            print(f"Error - could not save {img} -{e} ")
