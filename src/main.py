from concurrent.futures import ThreadPoolExecutor
from tkinter import Menu
from clipboard_reader import ClipboardCache
from paste_utils import paste_text
from word_menuitem import WordMenuItem
import rumps
import uuid
import pyperclip


class ClipboardHistoryApp(object):
    EMPTY_MENU_ITEM = WordMenuItem(title="No copied words")

    def __init__(self, title: str):
        self.app = rumps.App(title, icon="assets/copy.png", template=True, quit_button=None)
        self.menu_footer = [
            rumps.separator,
            rumps.MenuItem("Quit", lambda x: rumps.quit_application(), key="Q")]
        self.word_cache = ClipboardCache()
        self.empty = True
        self.latest_word = self.EMPTY_MENU_ITEM
        self.app.menu = [self.latest_word, *self.menu_footer]
        executor = ThreadPoolExecutor(1)
        executor.submit(self.__watch_clipboard__)


    def __watch_clipboard__(self):
            while True:
                try:
                    print("Watching for new word...")
                    new_word: str = pyperclip.waitForNewPaste()
                    print(f"Adding new word: {new_word}")
                    self.__update_words__(new_word)

                except pyperclip.PyperclipTimeoutException as e:
                    print(e)


    def run(self):
        self.app.run()


    def __update_words__(self, word):
        try:
            self.word_cache.update_clipboard(word)
            new_menuitem = WordMenuItem(
                title=word, callback=self.word_callback)

            self.app.menu.clear()
            self.app.menu = [WordMenuItem(title=cached_word, callback=self.word_callback, key=str(idx+1))
                                for idx, cached_word in enumerate(self.word_cache.get_words())] + self.menu_footer

            self.latest_word = new_menuitem

        except Exception as e:
            print(e)


    def word_callback(self, sender):
        paste_text(sender.word)

if __name__ == "__main__":
    ClipboardHistoryApp("Clipboard History").run()
