import rumps
from utils import word_size_bytes

class WordMenuItem(rumps.MenuItem):
    def __init__(self, expiry: float, display_length: int=30, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.word = self.title
        self.title = self.word[:display_length] + ("..." if len(self.word) > display_length else "")
        self.expiry = expiry
        self.size = word_size_bytes(self.word)