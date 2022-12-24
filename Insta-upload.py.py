import os
import instagram_private_api as insta_api
from PIL import Image

# Replace these with your own Instagram login credentials
USERNAME = 'xxxxxxxx'
PASSWORD = 'xxxxxxxx'

# Replace this with the path to your folder of images
IMAGE_FOLDER = 'images/'

# Authenticate with Instagram API
api = insta_api.Client(USERNAME, PASSWORD)

# Loop through the images in the folder
for filename in os.listdir(IMAGE_FOLDER):
  # Check that the file is an image
  if filename.endswith('.jpg') or filename.endswith('.png'):
    # Open the image file
    im = Image.open(f'{IMAGE_FOLDER}/{filename}')
    # Get the width and height of the image
    width, height = im.size
    # Check that the dimensions are within the allowed range
    if 320 <= width <= 1080 and 320 <= height <= 1350:
      # Upload the image to Instagram
      api.post_photo(f'{IMAGE_FOLDER}/{filename}', size=(width, height), caption='Drop a like if this speaks to you. #spreadpositivity #motivationoftheday #positivityiskey #mindsetmatters #inspiration #inspirationalquotes #keytosuccess #mindsetcoach #inspirational #mindsetshift #mindsetiseverything #successtips #moneymindset #motivationalquotesoftheday #motivationalquotes #inspirationalquote #inspirations #motivation101 #successmindset #successquotes #morningmotivation #quoteoftheday #motivation #inspiration')
    else:
      print(f'{filename} has invalid dimensions ({width}x{height}) and will not be uploaded.')

print('Done uploading images!')
