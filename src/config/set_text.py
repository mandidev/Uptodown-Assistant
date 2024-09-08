

def txt_start(username:str):
    return f"""
**
Estimado {username} 😊,
Le damos la bienvenida a Uptodown Assistant 🤖, nuestro Bot de Telegram, donde podrá descargar archivos de Uptodown de forma rápida y segura 📥. Estamos aquí para ofrecerle una experiencia eficiente y satisfactoria.
    
Si tiene alguna pregunta, no dude en contactarnos 💬.

__Atentamente,
@MandiCoder__ 🌟
**
""" 

def txt_caption(
    author:str,
    categoria:str,
    descargas:str,
    enlace:str,
    fecha:str,
    sistema_operativo:str,
    tamano:str,
    sha256:str
):
    txt =    "**🌐 Autor: **" + author
    txt += "**\n📱 Categoría: **" + categoria
    txt += "**\n⬇️ Descargas: **" + descargas
    txt += "**\n🔗 Enlace de descarga: **" + enlace
    txt += "**\n📅 Fecha: **" + fecha
    txt += "**\n📦 Tamaño: **" + tamano
    txt += "**\n📲 Sistema operativo: **" + sistema_operativo
    txt += "**\n🔒 SHA256: **" + f"`{sha256}`" 
    return txt