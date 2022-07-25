# // IMPORT
from kivy.app import App
from lib.TextInput import TextInputCustom, BoxLayout


# // RUN
if __name__ == "__main__":
    class Main(App):
        def __init__(self, **kwargs):
            # Local variable
            self.Sampled: bool = False

            super(Main, self).__init__(**kwargs)

        def build(self):
            # App arguments
            self.title = "Debugging // Line Numbers"

            # UIX
            self.layout = BoxLayout()
            self.MyText = TextInputCustom(width_line=36)
            # self.MyText.SetText("(Drag & Drop some files...)", end="\n"*2)
            # self.MyText.AddText("I hope was useful.")

            # # Debug: Changing color on click inside and outside of text input
            # self.MyText.binding(focus=self.on_focus)

            self.layout.add_widget(self.MyText)

            return self.layout

        def on_focus(self, instance, value):
            # As a hint just for you to know from where kivy is take it
            # kivy can use and fonts from your OS and is looking for an TTF extension
            # Font: comic   -> "C:\Windows\Fonts\Comic Sans MS\comic.ttf"
            # Font: symbol  -> "C:\Windows\Fonts\Symbol Regular\symbol.ttf"

            if value:
                # TODO: Fix cursor jump when font (name and/or size) changing on focus
                self.MyText.Theme(  # font_name="comic", font_size=18,
                    color_line="#313335", bg_line="#606366",
                    color_text="#2B2B2B", bg_text="#A9B7C6")

                if not self.Sampled:
                    with open(__file__, mode="r", encoding="UTF-8") as file:
                        self.MyText.SetText(file.read())
                        self.Sampled = True
                # Debug non-custom values
                # self.MyText.Theme(halign="right", cursor_width=10, cursor_color=[1,0,0,1])
            else:
                self.MyText.Theme(  # font_name="symbol", font_size=12,
                    color_line="#606366", bg_line="#313335",
                    color_text="#A9B7C6", bg_text="#2B2B2B")


    Main().run()