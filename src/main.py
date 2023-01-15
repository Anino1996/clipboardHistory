from concurrent.futures import ThreadPoolExecutor
from tkinter import Menu
import time
from clipboard_reader import ClipboardCache
from word_menuitem import WordMenuItem
import rumps
import pyperclip


class ClipboardHistoryApp(object):

    def __init__(self, title: str):
        self.app = rumps.App(title, icon="assets/copy.png", template=True, quit_button=None)
        self.menu_footer = [
            rumps.separator,
            rumps.MenuItem("Quit", lambda x: rumps.quit_application(), key="Q")]
        self.word_cache: ClipboardCache = ClipboardCache()
        self.app.menu = [*self.word_cache.get_words(), *self.menu_footer]
        self._cache_updating: bool = False
        ThreadPoolExecutor(1).submit(self.__watch_clipboard__)
        ThreadPoolExecutor(1).submit(self.__remove_expired__)

    def __watch_clipboard__(self):
            while True:
                try:
                    print("Watching for new word...")
                    new_word: str = pyperclip.waitForNewPaste()
                    print(f"Adding new word: {new_word}")
                    self.__update_words__(new_word)

                except pyperclip.PyperclipTimeoutException as e:
                    print(e)


    def __remove_expired__(self):
        while True:
            time.sleep(1800)
            if not self._cache_updating:
                
                print("Removing Expired values.")
                try:
                    self._cache_updating = True
                    self.word_cache.remove_expired()
                    self._update_appmenu()

                except Exception as e:
                    print(e)
                
                finally:
                    self._cache_updating = False


    def __update_words__(self, word):
        while self._cache_updating:
            time.sleep(1)

        try:
            self._cache_updating = True
            self.word_cache.update_clipboard(word)
            self._update_appmenu()

        except Exception as e:
            print(e)

        finally:
            self._cache_updating = False


    def _update_appmenu(self):
        self.app.menu.clear()
        self.app.menu = [*self.word_cache.get_words(), *self.menu_footer]



    def run(self):
        self.app.run()

if __name__ == "__main__":
    ClipboardHistoryApp("Clipboard History").run()
