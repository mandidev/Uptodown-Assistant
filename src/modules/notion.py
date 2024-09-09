import notion_client
import datetime
import os


def log_to_notion(title:str, message:str):
    notion = notion_client.Client(auth=os.getenv('NOTION_TOKEN'))
    fecha_hora = datetime.datetime.now().isoformat()

    new_record = {
        'parent': {'database_id': os.getenv('DATABASE_ID')},
        'properties': {
            'Tipo': {'title': [{'text': {'content': str(title)}}]},
            'Fecha y Hora': {'date': {'start': fecha_hora, 'end': fecha_hora}},
            'Mensaje': {'rich_text': [{'text': {'content': str(message)}}]}
        }
    }
    
    try:
        notion.pages.create(**new_record)
    except Exception as e:
        print("Error al registrar el error en Notion:", e)
        