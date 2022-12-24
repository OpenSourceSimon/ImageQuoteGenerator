from myigbot import MyIGBot

bot = MyIGBot('xxxxxxxxx', 'xxxxxxxxx')

upload = bot.upload_post('1.jpg', caption='Drop a like for daily quote. #quote')
print(upload)  # if the response code is 200 that means ok