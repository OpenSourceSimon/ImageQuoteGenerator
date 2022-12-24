from myigbot import MyIGBot

bot = MyIGBot('daily_.quoted', 'maheshishere9689')

image_filenames = ['2.jpg', '3.jpg', '4.jpg']

for image_filename in image_filenames:
    upload = bot.upload_post(image_filename, caption='Drop a like for daily quote. #quote')
    print(upload)  # if the response code is 200 that means ok
