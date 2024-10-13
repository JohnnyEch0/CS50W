import requests

import os
from urllib.parse import urlparse
from PIL import Image
import urllib



def download_image(image_url):
    """
    Tries downloading the image and returns True if succesful.
    """

    try:
        a = urlparse(image_url)
        file_name = os.path.basename(a.path)  # Output: 09-09-201315-47-571378756077.jpg
        dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(dir, "static/auctions/images", file_name)
        urllib.request.urlretrieve(image_url, path)
        return file_name
    
    except Exception as e:
        print("image dowloader:", e)
        return False

if __name__ == "__main__":
    download_image("https://www.dndbeyond.com/avatars/thumbnails/7/120/1000/1000/636284708068284913.jpeg")
    