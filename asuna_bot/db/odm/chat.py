from beanie import Document, Link
from typing import Optional
from pydantic import BaseModel
from .release import Release


class ChatConfig(BaseModel):
    submitter          : str  = "[SubsPlease]"
    show_alerts        : bool = True
    show_fhd           : bool = True
    show_hd            : bool = True
    show_sd            : bool = True
    show_direct_links  : bool = True
    show_magnet_links  : bool = True
    send_torrent_files : bool = True
    e2e_numbering      : bool = False


class Chat(Document):
    id      : int
    status  : str = None
    service_msg_id : int
    name    : str
    config  : ChatConfig = ChatConfig
    release : Optional[Link[Release]]
    
    class Settings:
        name = "chats"