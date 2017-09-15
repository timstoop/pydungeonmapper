# Disable multitouch as we do not need it
from kivy.config import Config

Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.app import App
from kivy.core.window import Window
from kivy.effects.scroll import ScrollEffect
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from kivytim.layout import SmartGridLayout
from dmrectangle import DMRectangle


class DMCanvas(BoxLayout):
    def __init__(self, **kwargs):
        super(DMCanvas, self).__init__(**kwargs)

        # Keep track of mouse
        self.last_child = 0

        # Create a scrollable view first
        view = ScrollView(size_hint=(None, None), size=(Window.width, Window.height), effect_cls=ScrollEffect,
                          bar_width=10)
        cols = 80
        rows = 60
        self.grid = SmartGridLayout(cols=cols, rows=rows, size_hint=(None, None))

        i = 0
        while i < cols * rows:
            t = DMRectangle()
            self.grid.add_widget(t)
            i = i + 1

        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.grid.bind(minimum_width=self.grid.setter('width'))
        view.add_widget(self.grid)
        self.add_widget(view)

        # Capture mouse location
        Window.bind(mouse_pos=self.my_mouse_pos)

    def my_mouse_pos(self, *args, **kwargs):
        pos = Window.mouse_pos
        child = self.grid.get_child_at(pos)
        if child != self.last_child:
            self.grid.children[child].set_selected(True)
            self.grid.children[self.last_child].set_selected(False)
            self.last_child = child
            self.canvas.ask_update()


class DungeonMapperApp(App):
    def build(self):
        return DMCanvas()


if __name__ == "__main__":
    DungeonMapperApp().run()
