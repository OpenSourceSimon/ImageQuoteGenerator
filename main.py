import json
import os
import textwrap
from datetime import datetime

import requests
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv


def import_env():
    load_dotenv()
    IMAGES_TO_GENERATE = os.getenv('IMAGES_TO_GENERATE')
    if IMAGES_TO_GENERATE is None or IMAGES_TO_GENERATE == '':
        IMAGES_TO_GENERATE = 1
    return IMAGES_TO_GENERATE


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
        data = requests.get('https://api.quotable.io/random').json()
        quote = data['content']
        author = data['author']
        SAVE_QUOTES_TO_FILE = os.getenv('SAVE_QUOTES_TO_FILE')
        quotes = open('quotes.json', 'r')
        if quote in quotes and SAVE_QUOTES_TO_FILE == 'True':
            print("\033[91m" + "Error: Quote already exists! \033[0m")
            get_quote()
        elif SAVE_QUOTES_TO_FILE == 'True':
            with open('quotes.json', 'r') as f:
                data = json.load(f)
                data.append({
                    'quote': quote,
                    'author': author
                })
            with open('quotes.json', 'w') as f:
                json.dump(data, f)
        else:
            pass
        print("\033[92m" + "Quote found! \033[0m")
        print("\033[92m" + quote + " - " + author + "\033[0m")
        return quote, author
    except KeyError:
        print("\033[91m" + "Error: Quote not found! \033[0m")
        get_quote()


def create_image(quote, author, i, folder):
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
        font = ImageFont.truetype('fonts/Roboto-Italic.ttf', int(font_size))
        font2 = ImageFont.truetype('fonts/Roboto-Bold.ttf', int(font_size))
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
        # If file already exists, add a number to the end of the file. Check again if the file exists and add a number to the end of the file.
        for i in range(100):
            if os.path.exists(f'{folder}/{i}.jpg'):
                continue
            else:
                image.save(f'{folder}/{i}.jpg')
                break
        print(i)
        print("\033[92m" + "Image created! \033[0m")
    except KeyError:
        print("\033[91m" + "Error: Image not created! \033[0m")
        return None


def create_folder():
    # Get the date
    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    hour = now.strftime("%H")
    if not os.path.exists(f'images/{date}/{hour}h - {os.getenv("CATEGORY")}'):
        os.makedirs(f'images/{date}/{hour}h - {os.getenv("CATEGORY")}')
    return f'images/{date}/{hour}h - {os.getenv("CATEGORY")}'


if __name__ == '__main__':
    print("\033[92m" + "Starting... \033[0m")
    IMAGES_TO_GENERATE = import_env()
    print("\033[92m" + "Environment variables imported! \033[0m")
    folder = create_folder()
    for i in range(int(IMAGES_TO_GENERATE)):
        quote, author = get_quote()
        create_image(quote, author, i, folder)
