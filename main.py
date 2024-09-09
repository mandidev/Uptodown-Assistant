from src.modules.bot_init import Bot
from src.modules.get_url import get_url
from src.config import set_text
from src.modules.notion import log_to_notion
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
    log_to_notion("COMANDO START", f"{message.from_user.username}")


@app.on_message(filters.text)
def download_data(client:Client, message:Message):
    
    patron = r'^https://.*\.uptodown\.com/.*'
    url = message.text
    log_to_notion("LOG", f"From: {message.from_user.username}\nEnlace enviado: {url}")
    
    if match(patron, url):
        try:
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
        except Exception as e:
            print("ERROR", e)
            log_to_notion("ERROR", e)
        
        try:
            message.reply_photo(
                data['Icono'],
                caption=caption,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="☁️ Subir a Telegram", callback_data=data['Enlace corto'])]
                ])
            )
        except Exception as e:
            print("ERROR", e)
            log_to_notion("ERROR", e)
        
        
        
@app.on_callback_query()
def download_file(client:Client, callback:CallbackQuery):
    message:Message = callback.message
    message.delete()
    
    username = callback.from_user.username
    caption = message.caption
    caption_entities = message.caption_entities
    
    try:
        msg = message.reply_sticker("src/static/uploading.tgs")
        short = Shortener()
        url = short.isgd.expand(callback.data)
        log_to_notion("LOG", f"From {username}\nDescargando archivo")
        file = download(url)
        
        log_to_notion("LOG", f"From {username}\nEnviando archivo a Telegram")
        message.reply_document(
            document=file,
            caption_entities=caption_entities,
            caption=caption
        )
        msg.delete()
        unlink(file)
    except Exception as e:
        print("ERROR", e)
        log_to_notion("ERROR", e)
    
        
bot.run()