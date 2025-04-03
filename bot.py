import telebot
‎from PIL import Image, ImageEnhance, ImageFilter
‎import requests
‎from io import BytesIO
‎from rembg import remove
‎
‎TOKEN = "7551178049:AAHqym1yEKqmgl_BBi-kd5P2xum4Fm866oY"
‎bot = telebot.TeleBot(TOKEN)
‎
‎@bot.message_handler(commands=['start'])
‎def send_welcome(message):
‎    bot.send_message(message.chat.id, "👋 Welcome! I am ArtifexAI, your AI-powered image editing bot. Send me a photo to get started!")
‎
‎@bot.message_handler(content_types=['photo'])
‎def handle_image(message):
‎    bot.send_message(message.chat.id, "📸 You have sent an image! I will process it soon.")
‎    
‎    # Get the image from the message
‎    photo = message.photo[-1]
‎    photo_file = bot.get_file(photo.file_id)
‎    photo_url = f'https://api.telegram.org/file/bot{TOKEN}/{photo_file.file_path}'
‎    image_data = requests.get(photo_url).content
‎
‎    # Open the image
‎    image = Image.open(BytesIO(image_data))
‎
‎    # Apply some basic effects (for example, brightness and contrast adjustment)
‎    enhancer = ImageEnhance.Brightness(image)
‎    image = enhancer.enhance(1.2)  # Increase brightness by 20%
‎
‎    enhancer = ImageEnhance.Contrast(image)
‎    image = enhancer.enhance(1.5)  # Increase contrast by 50%
‎
‎    # Apply Blur (as an example of effect 10)
‎    image = image.filter(ImageFilter.GaussianBlur(radius=5))  # Apply blur effect
‎
‎    # Save the edited image
‎    image.save("edited_image.jpg")
‎
‎    # Send the edited image back to the user
‎    with open("edited_image.jpg", "rb") as photo_file:
‎        bot.send_photo(message.chat.id, photo_file)
‎
‎@bot.message_handler(commands=['remove_bg'])
‎def remove_background(message):
‎    bot.send_message(message.chat.id, "🔍 Removing the background...")
‎
‎    # Get the image from the message
‎    photo = message.photo[-1]
‎    photo_file = bot.get_file(photo.file_id)
‎    photo_url = f'https://api.telegram.org/file/bot{TOKEN}/{photo_file.file_path}'
‎    image_data = requests.get(photo_url).content
‎
‎    # Open and remove the background
‎    input_image = Image.open(BytesIO(image_data))
‎    output_image = remove(input_image)
‎
‎    # Save and send the output image
‎    output_image.save("no_background_image.png")
‎    with open("no_background_image.png", "rb") as output_file:
‎        bot.send_photo(message.chat.id, output_file)
‎
‎bot.polling()
‎
