from src.modules.bot_init import Bot
from src.modules.get_url import get_url
from src.config import set_text
from pyrogram import filters, Client
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyshorteners import Shortener
from re import match
from os import unlink
from wget import download

bot = Bot()
app = bot.app

@app.on_message(filters.command("start"))
def start(client:Client, message:Message):
    message.reply(set_text.txt_start(message.from_user.username))



@app.on_message(filters.text)
def download_data(client:Client, message:Message):
    patron = r'^https://.*\.uptodown\.com/.*'
    url = message.text
    
    if match(patron, url):
        sms:Message = message.reply("⏳ **Obteniendo informacion...**")
        data = get_url(url)
        sms.delete()
        
        caption = set_text.txt_caption(
            data['Autor'],
            data['Categoría'],
            data['Descargas'],
            data['Enlace corto'],
            data['Fecha'],
            data['Sistema operativo'],
            data['Tamaño'],
            data['SHA256']
        )
        
        message.reply_photo(
            data['Icono'],
            caption=caption,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="☁️ Subir a Telegram", callback_data=data['Enlace corto'])]
            ])
        )
        
        
        
@app.on_callback_query()
def download_file(client:Client, callback:CallbackQuery):
    message:Message = callback.message
    message.delete()
    
    caption = message.caption
    caption_entities = message.caption_entities
    
    msg = message.reply_sticker("src/static/uploading.tgs")
    short = Shortener()
    url = short.isgd.expand(callback.data)
    file = download(url)
    
    message.reply_document(
        document=file,
        caption_entities=caption_entities,
        caption=caption
    )
    msg.delete()
    unlink(file)
    
        
bot.run()