import telebot
import requests
import re
import os
from flask import Flask, request

TOKEN = "8053069809:AAFpMKtnbIT0-2zKiQ38rKFurpDW1T4rnDE"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def get_instagram_video_url(insta_url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        r = requests.get(insta_url, headers=headers)
        video_urls = re.findall('"video_url":"(.*?)"', r.text)
        if video_urls:
            return video_urls[0].replace("\u0026", "&").replace("\", "")
        else:
            return None
    except:
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Instagram video havolasini yuboring!")

@bot.message_handler(func=lambda message: "instagram.com" in message.text)
def download_instagram_video(message):
    url = message.text.strip()
    bot.send_chat_action(message.chat.id, 'upload_video')
    video_url = get_instagram_video_url(url)
    if video_url:
        video_data = requests.get(video_url).content
        with open("video.mp4", "wb") as f:
            f.write(video_data)
        with open("video.mp4", "rb") as video:
            bot.send_video(message.chat.id, video)
        os.remove("video.mp4")
    else:
        bot.reply_to(message, "❌ Video topilmadi yoki yopiq profil bo'lishi mumkin.")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/", methods=["GET"])
def index():
    return "Bot ishlayapti!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
