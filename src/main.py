from threading import Thread, Event
from clipboard_reader import ClipboardCache
import rumps
import time
import pyperclip


class ClipboardHistoryApp(object):

    def __init__(self, title: str):
        self.app = rumps.App(title, icon="assets/copy.png", template=True, quit_button=None)
        self.menu_footer = [
            rumps.separator,
            rumps.MenuItem("Quit", lambda x: rumps.quit_application(), key="Q")]
        self.word_cache: ClipboardCache = ClipboardCache()
        self.app.menu = [*self.word_cache.get_words(), *self.menu_footer]
    
        self._cancellation_event: Event = Event()
        self._history_updater_thread: Thread = Thread(name="ClipboardHistoryWatcher", target=self.__watch_clipboard__, daemon=True)
        self._history_cleaner_thread: Thread = Thread(name="ClipboardHistoryCleaner", target=self.__remove_expired__, daemon=True)

    def __watch_clipboard__(self):
        while not self._cancellation_event.is_set():
            try:
                print("Watching for new word...")
                new_word: str = pyperclip.waitForNewPaste()
                print(f"Adding new word: {new_word}")
                self.__update_words__(new_word)

            except pyperclip.PyperclipTimeoutException as e:
                print(e)


    def __remove_expired__(self):
        while not self._cancellation_event.is_set():
            time.sleep(1800)
            print("Removing Expired values.")
            self.word_cache.safe_remove_expired()
            self._update_appmenu()


    def __update_words__(self, word):
        self.word_cache.update_clipboard(word)
        self._update_appmenu()


    def _update_appmenu(self):
        self.app.menu.clear()
        self.app.menu = [*self.word_cache.get_words(), *self.menu_footer]


    def run(self):
        self._history_cleaner_thread.start()
        self._history_updater_thread.start()
        self.app.run()


    def quit(self):
        self._cancellation_event.set()
        self._history_cleaner_thread.join()
        self._history_updater_thread.join()
        rumps.quit_application()


if __name__ == "__main__":
    ClipboardHistoryApp("Clipboard History").run()
