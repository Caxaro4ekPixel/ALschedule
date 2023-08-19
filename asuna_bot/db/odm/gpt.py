from beanie import Document, Link
from .chat import Chat
from .user import User

class ChatGPT(Document):
    model    : str
    request  : str
    response : str
    user     : Link[User]
    chat     : Link[Chat]
    
    class Settings:
        name = "chat_gpt"