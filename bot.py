from telegram.ext import Updater, CommandHandler
import requests
import re
import random
import os

PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ.get('BOT_TOKEN')

# Get dog image URL
# URL will give a json and the URL is under the url tag
def get_dog_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


# Get cat image URL
# json has list indices, URL under index 0
def get_cat_url():
    contents = requests.get('https://api.thecatapi.com/v1/images/search').json()
    url = contents[0]['url']
    return url


# RandomDog API also generates gif and videos, so get only URL for images
def get_dog_image_url():
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_dog_url()
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url


# Sends a dog photo
# Change arguments from (bot, update) to (update, context) due to change in handlers
def boop(update, context):
    url = get_dog_image_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)


# Sends a cat photo
def floof(update, context):
    url = get_cat_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)


# Sends a dog photo and a message
def pat(update, context):
    chat_id = update.message.chat_id
    url = get_dog_image_url()
    context.bot.send_photo(chat_id=chat_id, photo=url)
    list_text = ['Woof', 'Arrfff', 'yap', 'Aaawooof',
                 'The dog sticks out his tongue and asks for more pats.',
                 'The dog nudges your hand with their head.',
                 'The dog shakes their tail like a helicopter.']
    text_sent = random.choice(list_text)
    context.bot.send_message(chat_id=chat_id, text=text_sent)


# Sends a cat photo and a message
def scratch(update, context):
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    url = get_cat_url()
    context.bot.send_photo(chat_id=chat_id, photo=url)
    list_text = ['Puurrrrr', 'Meoowww', 'Meow meow meow', 'The cat ran away.',
                 'The cat starts kneading you their front paws.',
                 'The cat nudges your hand with their head.']
    text_sent = random.choice(list_text)
    context.bot.send_message(chat_id=chat_id, text=text_sent)


# Sends a cat photo and a message
def inspire(update, context):
    chat_id = update.message.chat_id
    contents = requests.get('https://zenquotes.io/api/random').json()
    quote = contents[0]['q']
    context.bot.send_message(chat_id=chat_id, text=quote)


# Sends a cat photo and a message
# Some quotes from
# https://ideas.hallmark.com/articles/encouragement-ideas/encouragement-messages-what-to-write-in-an-encouragement-card/
def encourage(update, context):
    chat_id = update.message.chat_id
    list_text = ['Good luck today! I know you’ll do great.',
                 'Be good to yourself. And let others be good to you, too.',
                 'You’re doing exactly what you should be doing. Hang in there.',
                 'Hearts take time to heal. Be gentle with yourself.',
                 'It’s okay not to be okay.',
                 'Just wanted to send you a smile today.',
                 'I believe in you! And unicorns. But mostly you!',
                 'This, too, shall pass. And hopefully not like a kidney stone.',
                 'You and bacon are in my thoughts a lot these days. Hey, it’s not all about you, you know.',
                 'You can get through this. Take it from me. I’m very wise and stuff. Like, I\'m a bot.',
                 'At a time like this, don’t even bother with a dish. Just grab a spoon and start shoveling '
                 'ice cream straight from the carton.',
                 'Life is meaningless so don’t worry about making the wrong choice. There is no right or wrong path, '
                 'so travel down whichever one you please.']
    text_sent = random.choice(list_text)
    context.bot.send_message(chat_id=chat_id, text=text_sent)


# Tells a dad joke
# Referenced from https://github.com/chrispinkney/DAD-JOKE-3000/blob/master/dad-joke-3000.py
def jokes(update, context):
    chat_id = update.message.chat_id
    url = "https://icanhazdadjoke.com/search"

    res = requests.get(
        url,
        headers={"Accept": "application/json"},
    ).json()
    results = res["results"]
    num_jokes = len(results)

    if num_jokes > 0:
        index = random.randint(0, 10)
        joke = results[index]["joke"]
    else:
        joke = 'No jokes found.'

    context.bot.send_message(chat_id=chat_id, text=joke)


# Main function to be called
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('boop', boop))
    dp.add_handler(CommandHandler('floof', floof))
    dp.add_handler(CommandHandler('scratch', scratch))
    dp.add_handler(CommandHandler('pat', pat))
    dp.add_handler(CommandHandler('inspire', inspire))
    dp.add_handler(CommandHandler('encourage', encourage))
    dp.add_handler(CommandHandler('jokes', jokes))
    
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url="https://encouraging.herokuapp.com/" + TOKEN)    

    updater.idle()


# Call the main function
if __name__ == '__main__':
    main()
