from pyrogram import Client
from dotenv import load_dotenv
from os import getenv
from .webserver import keep_alive

load_dotenv()

class Bot():
    def __init__(self) -> None:
        print(getenv('API_ID'), getenv('API_HASH'), getenv('BOT_TOKEN'))
        self.app = Client(
            "UptodownBot", 
            api_id=getenv('API_ID'), 
            api_hash=getenv('API_HASH'),
            bot_token=getenv('BOT_TOKEN')
        )
        
    def run(self):
        keep_alive()
        self.app.run()
        
        