from beanie import Document

class BotConfig(Document):
    nyaa_rss_interval : int = 180
    nyaa_rss_last_id  : int
    timezone          : str = "Europe/Moscow"
    
    class Settings:
        name = "bot_config"
