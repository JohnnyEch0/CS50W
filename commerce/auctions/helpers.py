import requests

def download_image(image_url):
    """
    Tries downloading the image and returns True if succesful.
    """

    try:
        img_data = requests.get(image_url).content
        with open('static/images/image_url', 'wb') as handler:
            handler.write(img_data)

        return True
    except Exception as e:
        return False


    