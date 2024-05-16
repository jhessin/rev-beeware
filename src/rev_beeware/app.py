"""
An offline reader for the REV bible.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
from toga.widgets.button import OnPressHandler

from rev_beeware.storage import Storage


class REVBeeware(toga.App):
    web_view: toga.WebView
    verse_input: toga.TextInput
    load_page: toga.Button.on_press
    storage: Storage

    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.

        Create a WebView to hold the generated text.
        """

        self.web_view = toga.WebView(
            style=Pack(flex=1)
        )
        self.verse_input = toga.TextInput(
            value="https://www.revisedenglishversion.com/", style=Pack(flex=1)
        )

        # This should provide the full layout of the app.
        main_box = toga.Box(
            children=[
                toga.Box(
                    children=[
                        self.verse_input,
                        toga.Button(
                            'Go',
                            on_press=self.load_page,
                            style=Pack(width=50, padding_left=5)
                        ),
                    ],
                    style=Pack(
                        direction=ROW,
                        alignment=CENTER,
                        padding=5,
                    ),
                ),
                self.web_view,
            ],
            style=Pack(direction=COLUMN),
        )
        self.storage = Storage(self)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def load_page(self, widget):
        """
        This executes when you hit the 'go' button.
        """
        # self.web_view.url = self.verse_input.value
        result = f" remote: {self.storage.remote_date} <br> local: {self.storage.local_date}"
        self.web_view.set_content('/', result)


def main():
    return REVBeeware()
