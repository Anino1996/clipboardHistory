from typing import List

class ClipboardCache:
    MAX_SIZE_BYTES: int = 10
    
    def __init__(self):
        self._words: List[str] = []
        self._cache_size: int = 0
        self.dropped_words_flag: bool = False
    
    def get_words(self) -> List[str]:
        return self._words
    
    def get_cache_size(self) -> int:
        return self._cache_size
    
    @classmethod
    def utf8len(cls, word: str) -> int:
        return len(word.encode("utf-8"))
    
    def update_clipboard(self, new_word: str) -> None:
        new_word_size: int = self.utf8len(new_word)
        
        if new_word_size > self.MAX_SIZE_BYTES:
            raise OverflowError("Value too big. Cannot add to list.")
        
        self.dropped_words_flag = self._cache_size + new_word_size > self.MAX_SIZE_BYTES
        
        while (self._cache_size + new_word_size) > self.MAX_SIZE_BYTES:
            self._cache_size -= self.utf8len(self._words.pop())
            
        self._words.insert(0, new_word)
        self._cache_size += new_word_size