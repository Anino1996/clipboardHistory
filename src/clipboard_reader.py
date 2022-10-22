from rumps import MenuItem
from typing import List
from datetime import datetime, timedelta
from word_menuitem import WordMenuItem
from utils import paste_text, word_size_bytes

class ClipboardCache:
    MAX_SIZE_BYTES: int = 100*1024*1024
    EMPTY_MENU_ITEM = MenuItem(title="No copied words")
    TTL: timedelta = timedelta(days=2)


    def __init__(self):
        self._words: List[WordMenuItem] = []
        self._cache_size: int = 0


    def get_words(self) -> List[WordMenuItem]:
        return self._words if not self.is_empty() else [self.EMPTY_MENU_ITEM]


    def get_cache_size(self) -> int:
        return self._cache_size


    def update_clipboard(self, new_word: str) -> None:
        new_word_size: int = word_size_bytes(new_word)

        self.remove_expired()
        
        if new_word_size > self.MAX_SIZE_BYTES:
            raise OverflowError("Value too big. Cannot add to list.")
        
        while (self._cache_size + new_word_size) > self.MAX_SIZE_BYTES:
            self._cache_size -= self._words.pop().size
            
        self._words.insert(0, WordMenuItem(
            title=new_word,
            expiry=(datetime.now() + self.TTL).timestamp(),
            callback=self.word_callback))
        
        self._cache_size += new_word_size


    def is_empty(self) -> bool:
        return len(self._words) <= 0
    

    def remove_expired(self):
        current_time: float = datetime.now().timestamp()
        while not self.is_empty() and self._words[-1].expiry < current_time:
            self._cache_size -= self._words.pop().size


    def word_callback(self, sender):
        paste_text(sender.word)