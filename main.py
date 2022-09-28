import os
import textwrap

import requests
import tweepy
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv


def import_env():
    load_dotenv()
    global CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    ACCESS_SECRET = os.getenv('ACCESS_SECRET')
    IMAGES_TO_GENERATE = os.getenv('IMAGES_TO_GENERATE')
    if IMAGES_TO_GENERATE is None or IMAGES_TO_GENERATE == '':
        IMAGES_TO_GENERATE = 1
    return CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, IMAGES_TO_GENERATE


def draw_multiple_line_text(image, text, font, text_color, text_start_height):
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=45)
    for line in lines:
        nothing1, nothing2, line_width, line_height = font.getbbox(line)
        # draw shadow on text
        draw.text(((image_width - line_width) / 2 + 2, y_text + 2),
                  line, font=font, fill=(0, 0, 0))
        draw.text(((image_width - line_width) / 2, y_text),
                  line, font=font, fill=text_color)
        y_text += line_height
    # Return the bottom pixel of the text
    return y_text


def get_quote():
    try:
        main = requests.get('https://api.quotable.io/random')
        data = main.json()
        quote = data['content']
        author = data['author']
        print("\033[92m" + "Quote found! \033[0m")
        print("\033[92m" + quote + " - " + author + "\033[0m")
        return quote, author
    except KeyError:
        print("\033[91m" + "Error: Quote not found! \033[0m")
        return None


def create_image(quote, author, i):
    try:
        resolution = os.getenv('RESOLUTION')
        category = os.getenv('CATEGORY')
        font_size = os.getenv('FONT_SIZE')
        if resolution is None or resolution == '' or not 'x' in resolution:
            resolution = (1080, 1080)
        image = Image.open(requests.get(f'https://source.unsplash.com/random/{resolution}?{category}', stream=True).raw)
        image = Image.open(requests.get(f'https://source.unsplash.com/random/{resolution}?{category}',
                                        stream=True).raw)  # Two times because the first one is always the same
        # The image not found image of Unsplash is 1200x800.
        if image.size == (1200, 800):
            print("\033[91m" + "Error: Image not found! \033[0m")
            return None
        image = image.resize((4000, 4000))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('fonts/Roboto-Italic.ttf', 150)
        font2 = ImageFont.truetype('fonts/Roboto-Bold.ttf', 150)
        if len(quote) > 350:
            text_start_height = (image.height - font.getbbox(quote)[3]) / 2 - 500
        elif len(quote) > 250:
            text_start_height = (image.height - font.getbbox(quote)[3]) / 2 - 200
        elif len(quote) > 150:
            text_start_height = (image.height - font.getbbox(quote)[3]) / 2 - 50
        else:
            text_start_height = (image.height - font.getbbox(quote)[3]) / 2
        end = draw_multiple_line_text(image, quote, font, text_color=(255, 255, 255),
                                      text_start_height=text_start_height)
        # Draw the author shadow
        draw.text(((image.width - font2.getbbox(author)[2]) / 2 + 2, end + 50),
                  author, font=font2, fill=(0, 0, 0))
        # Draw the author
        draw.text(((image.width - font2.getbbox(author)[2]) / 2, end + 50), author, font=font2, fill=(255, 255, 255))
        if not os.path.exists('images'):
            os.makedirs('images')
        image.save(f'images/quote_{i}.jpg')
        print("\033[92m" + "Image created! \033[0m")
    except KeyError:
        print("\033[91m" + "Error: Image not created! \033[0m")
        return None


# Tweet the image
def tweet_image(i):
    if CONSUMER_KEY == '' or CONSUMER_SECRET == '' or ACCESS_KEY == '' or ACCESS_SECRET == '' or CONSUMER_KEY is None or CONSUMER_SECRET is None or ACCESS_KEY is None or ACCESS_SECRET is None:
        print("\033[91m" + "Please fill in the credentials first in the .env file! \033[0m")
        exit()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    try:
        imagePath = f"images/quote{i}.jpg"
        status = "#motivation #inspiration #quote"

        api.update_with_media(imagePath, status)
        print("\033[94m" + "Tweeted! \033[0m")
    except tweepy.TweepError as e:
        if e.api_code == 187:
            print("\033[91m" + "Error: Duplicate tweet! \033[0m")
            return None
        elif e.api_code == 186:
            print("\033[91m" + "Error: Tweet is too long! \033[0m")
            return None
        elif e.api_code == 326:
            print("\033[91m" + "Error: Image is too large! \033[0m")
            return None
        else:
            if 'Failed to send request: Only unicode objects are escapable.' in e.reason:
                print("\033[91m" + "Error: Credentials are not correct! \033[0m")
                exit()
                return None
            print("\033[91m" + "Error: Something went wrong! \033[0m")
            print(e)
            return None


if __name__ == '__main__':
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, IMAGES_TO_GENERATE = import_env()
    for i in range(int(IMAGES_TO_GENERATE)):
        quote, author = get_quote()
        create_image(quote, author, i)
        # tweet_image(i)
