# Disable multitouch as we do not need it
from kivy.config import Config

Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.app import App
from kivy.core.window import Window
from kivy.effects.scroll import ScrollEffect
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from kivytim.layout import SmartGridLayout

OPPOSITE_SIDE = {
    'north': 'south',
    'south': 'north',
    'east': 'west',
    'west': 'east',
    'northwest': 'southeast',
    'northeast': 'southwest',
    'southwest': 'northeast',
    'southeast': 'northwest'
}


class DMRectangle(ButtonBehavior, Widget):
    def __init__(self, linesize=18, **kwargs):
        super(DMRectangle, self).__init__(**kwargs)
        # Keep track of linesize to know how large we are
        self.linesize = linesize
        # This makes sure we have a fixed size
        self.size = (self.linesize, self.linesize)
        self.size_hint = (None, None)
        # Draw diagonal lines
        self.wall = True
        # Keep track of wall sides
        self.empty_sides = set()
        # Is the mouse hovering over us?
        self.selected = False

    def add_empty_side(self, side):
        """Sides are defined as follows:

           1 2 3
           8   4
           7 6 5
        """
        if side == 'east':
            self.empty_sides.add(4)
        elif side == 'west':
            self.empty_sides.add(8)
        elif side == 'north':
            self.empty_sides.add(2)
        elif side == 'south':
            self.empty_sides.add(6)
        elif side == 'northwest':
            self.empty_sides.add(1)
        elif side == 'northeast':
            self.empty_sides.add(3)
        elif side == 'southwest':
            self.empty_sides.add(7)
        elif side == 'southeast':
            self.empty_sides.add(5)

    def remove_empty_side(self, side):
        """Sides are defined as follows:

           1 2 3
           8   4
           7 6 5
        """
        if side == 'east' and 4 in self.empty_sides:
            self.empty_sides.remove(4)
        elif side == 'west' and 8 in self.empty_sides:
            self.empty_sides.remove(8)
        elif side == 'north' and 2 in self.empty_sides:
            self.empty_sides.remove(2)
        elif side == 'south' and 6 in self.empty_sides:
            self.empty_sides.remove(6)
        elif side == 'northwest' and 1 in self.empty_sides:
            self.empty_sides.remove(1)
        elif side == 'northeast' and 3 in self.empty_sides:
            self.empty_sides.remove(3)
        elif side == 'southwest' and 7 in self.empty_sides:
            self.empty_sides.remove(7)
        elif side == 'southeast' and 5 in self.empty_sides:
            self.empty_sides.remove(5)

    def redraw(self):
        x = self.pos[0]
        y = self.pos[1]
        size = self.linesize

        with self.canvas:
            self.canvas.clear()
            Color(1, 1, 1, 1)
            Rectangle(pos=(x, y), size=(self.linesize, self.linesize))
            if self.wall:
                self.draw_wall(x, y, size)

        if self.selected:
            with self.canvas.after:
                selected_points = [x + 2, y + 2, x + size - 4, y, x + size - 4, y + size - 4, x + 2, y + size - 4,
                                   x + 2, y + 2]
                Color(1, 0, 0, 0.5)
                Line(points=selected_points)

    def draw_wall(self, x, y, size):
        halfsize = size / 2.0
        points = [x, y, x + size, y, x + size, y + size, x, y + size, x, y]
        diagonal_1 = [x + halfsize, y, x + size, y + halfsize]
        diagonal_2 = [x + size, y + size, x, y]
        diagonal_3 = [x, y + halfsize, x + halfsize, y + size]

        with self.canvas:
            Color(0, 0, 0, 1)
            Line(points=points)
            Color(0.2, 0.2, 0.2, 0.3)
            Line(points=[diagonal_1])
            Line(points=[diagonal_2])
            Line(points=[diagonal_3])
            if len(self.empty_sides) > 0:
                self.draw_empty_sides(x, y, size)

    def draw_empty_sides(self, x, y, size):
        partsize = size / 3.0
        rectsize = partsize + 1

        with self.canvas:
            if 1 in self.empty_sides or 2 in self.empty_sides or 8 in self.empty_sides:
                Color(1, 1, 1, 1)
                Rectangle(pos=(x - 1, y + (2 * partsize)), size=(rectsize, rectsize))
                Color(0, 0, 0, 1)
                if 8 not in self.empty_sides:
                    Line(points=[x - 1, y + (2 * partsize), x + partsize, y + (2 * partsize)])
                if 2 not in self.empty_sides:
                    Line(points=[x + partsize, y + (2 * partsize) - 1, x + partsize, y + (3 * partsize)])
            if 2 in self.empty_sides:
                Color(1, 1, 1, 1)
                Rectangle(pos=(x + partsize, y + (2 * partsize)), size=(rectsize, rectsize))
                Color(0, 0, 0, 1)
                Line(points=[x + partsize, y + (2 * partsize), x + (2 * partsize), y + (2 * partsize)])
            if 3 in self.empty_sides or 2 in self.empty_sides or 4 in self.empty_sides:
                Color(1, 1, 1, 1)
                Rectangle(pos=(x + (2 * partsize), y + (2 * partsize)), size=(rectsize, rectsize))
                Color(0, 0, 0, 1)
                if 4 not in self.empty_sides:
                    Line(points=[x + (2 * partsize), y + (2 * partsize), x + (3 * partsize), y + (2 * partsize)])
                if 2 not in self.empty_sides:
                    Line(points=[x + (2 * partsize), y + (2 * partsize), x + (2 * partsize), y + (3 * partsize)])
            if 4 in self.empty_sides:
                Color(1, 1, 1, 1)
                Rectangle(pos=(x + (2 * partsize) - 1, y + partsize), size=(rectsize, rectsize))
                Color(0, 0, 0, 1)
                Line(points=[x + (2 * partsize), y + partsize, x + (2 * partsize), y + (2 * partsize)])
            if 5 in self.empty_sides or 4 in self.empty_sides or 6 in self.empty_sides:
                Color(1, 1, 1, 1)
                Rectangle(pos=(x + (2 * partsize), y), size=(rectsize, rectsize))
                Color(0, 0, 0, 1)
                if 6 not in self.empty_sides:
                    Line(points=[x + (2 * partsize), y, x + (2 * partsize), y + partsize])
                if 4 not in self.empty_sides:
                    Line(points=[x + (2 * partsize) - 1, y + partsize, x + (3 * partsize) + 1, y + partsize])
            if 6 in self.empty_sides:
                Color(1, 1, 1, 1)
                Rectangle(pos=(x + partsize, y), size=(rectsize, rectsize))
                Color(0, 0, 0, 1)
                Line(points=[x + partsize, y + partsize, x + (2 * partsize) + 1, y + partsize])
            if 7 in self.empty_sides or 6 in self.empty_sides or 8 in self.empty_sides:
                Color(1, 1, 1, 1)
                Rectangle(pos=(x - 1, y), size=(rectsize, rectsize))
                Color(0, 0, 0, 1)
                if 8 not in self.empty_sides:
                    Line(points=[x - 1, y + partsize, x + partsize, y + partsize])
                if 6 not in self.empty_sides:
                    Line(points=[x + partsize, y + partsize, x + partsize, y])
            if 8 in self.empty_sides:
                Color(1, 1, 1, 1)
                Rectangle(pos=(x - 1, y + partsize), size=(rectsize, rectsize))
                Color(0, 0, 0, 1)
                Line(points=[x + partsize, y + partsize, x + partsize, y + (2 * partsize) + 1])

    def trigger_change(self, change, action, on_side):
        if change == 'wall':
            if action == 'add':
                self.add_empty_side(on_side)
            elif action == 'remove':
                self.remove_empty_side(on_side)
            else:
                raise Exception('Unknown action %s' % action)
        else:
            raise Exception('Unknown change %s' % change)
        # Always end with a redraw
        self.redraw()

    def trigger_neighbours(self, change, action):
        neighbours = self.parent.get_my_neighbours(self)
        # trigger them all and if they change, they should trigger their neighbours as well if needed
        for side, value in neighbours.items():
            if value is not None:
                # Trigger the widget at that specific index
                self.parent.children[value].trigger_change(change, action, OPPOSITE_SIDE[side])

    def set_selected(self, selected):
        self.selected = selected
        self.redraw()

    def on_pos(self, instance, value):
        self.redraw()

    def on_press(self):
        if self.wall:
            self.wall = False
            self.trigger_neighbours('wall', 'add')
        else:
            self.wall = True
            self.trigger_neighbours('wall', 'remove')
        self.redraw()
        self.canvas.ask_update()
        return False


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
