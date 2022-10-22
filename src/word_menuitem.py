import rumps

class WordMenuItem(rumps.MenuItem):
    def __init__(self, display_length=30, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.word = self.title
        self.title = self.word[:display_length] + ("..." if len(self.word) > display_length else "")