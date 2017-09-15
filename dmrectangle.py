from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Rectangle
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget

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

GRIDSIZE = 18


class DMRectangle(ButtonBehavior, Widget):
    selected = BooleanProperty(False)

    def __init__(self, linesize=GRIDSIZE, **kwargs):
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
                selected_points = [x + 2, y + 2, x + size - 2, y + 2, x + size - 2, y + size - 2, x + 2, y + size - 2,
                                   x + 2, y + 2]
                Color(1, 0, 0, 0.5)
                Line(points=selected_points)
        else:
            with self.canvas.after:
                self.canvas.after.clear()

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
        partsize = size / 6.0

        # Top left piece
        #  ________
        # |_|____|_|    3 6
        # | |    | |  1 2 4 5
        # | |    | |
        # | |    | |
        # |_|____|_|  9 a d e
        # |_|____|_|  7 8 b c
        #

        (x1, y1) = (x - 1, y + (5 * partsize))
        (x2, y2) = (x + partsize, y + (5 * partsize))
        (x3, y3) = (x + partsize, y + size + 1)
        (x4, y4) = (x + (5 * partsize), y + (5 * partsize))
        (x5, y5) = (x + size + 1, y + (5 * partsize))
        (x6, y6) = (x + (5 * partsize), y + size + 1)
        (x7, y7) = (x - 1, y - 1)
        (x8, y8) = (x + partsize, y - 1)
        (x9, y9) = (x - 1, y + partsize)
        (xa, ya) = (x + partsize, y + partsize)
        (xb, yb) = (x + (5 * partsize), y - 1)
        (xc, yc) = (x + size + 1, y - 1)
        (xd, yd) = (x + (5 * partsize), y + partsize)
        (xe, ye) = (x + size + 1, y + partsize)

        with self.canvas:
            if 1 in self.empty_sides or 2 in self.empty_sides or 8 in self.empty_sides:
                Color(1, 1, 1, 1)
                Rectangle(pos=(x1, y1), size=(partsize + 1, partsize + 1))
                Color(0, 0, 0, 1)
                if 8 not in self.empty_sides:
                    Line(points=[x1, y1, x2, y2], width=1)
                if 2 not in self.empty_sides:
                    Line(points=[x2, y2, x3, y3], width=1)
            if 2 in self.empty_sides:
                Color(1, 1, 1, 1)
                Rectangle(pos=(x2, y2), size=(4 * partsize + 1, partsize + 1))
                Color(0, 0, 0, 1)
                Line(points=[x2, y2, x4, y4], width=1)
            if 3 in self.empty_sides or 2 in self.empty_sides or 4 in self.empty_sides:
                Color(1, 1, 1, 1)
                Rectangle(pos=(x4, y4), size=(partsize + 1, partsize + 1))
                Color(0, 0, 0, 1)
                if 4 not in self.empty_sides:
                    Line(points=[x4, y4, x5, y5], width=1)
                if 2 not in self.empty_sides:
                    Line(points=[x4, y4, x6, y6], width=1)
                    Color(0.9, 0.9, 0.9, 1)
                    Rectangle(pos=(x4, y4), size=(partsize, partsize+1))
            if 4 in self.empty_sides:
                Color(1, 1, 1, 1)
                Rectangle(pos=(xd, yd), size=(partsize + 1, 4 * partsize + 1))
                Color(0, 0, 0, 1)
                Line(points=[xd, yd, x4, y4], width=1)
                Color(0.9, 0.9, 0.9, 1)
                Rectangle(pos=(xd, yd), size=(partsize, 4 * partsize + 1))
            if 5 in self.empty_sides or 4 in self.empty_sides or 6 in self.empty_sides:
                Color(1, 1, 1, 1)
                Rectangle(pos=(xb, yb), size=(partsize + 1, partsize + 1))
                if not ((4 in self.empty_sides) and (6 in self.empty_sides)):
                    if 6 not in self.empty_sides:
                        Color(0.9, 0.9, 0.9, 1)
                    if 4 not in self.empty_sides:
                        Color(0.8, 0.8, 0.8, 1)
                    Rectangle(pos=(xb, yb), size=(partsize + 1, partsize))
                Color(0, 0, 0, 1)
                if 6 not in self.empty_sides:
                    Line(points=[xd, yd, xb, yb], width=1)
                if 4 not in self.empty_sides:
                    Line(points=[xd, yd, xe, ye], width=1)
            if 6 in self.empty_sides:
                Color(1, 1, 1, 1)
                Rectangle(pos=(x8, y8), size=(4 * partsize + 1, partsize + 1))
                Color(0, 0, 0, 1)
                Line(points=[xa, ya, xd, yd], width=1)
                Color(0.8, 0.8, 0.8, 1)
                Rectangle(pos=(x8, y8), size=(4 * partsize + 1, partsize))
            if 7 in self.empty_sides or 6 in self.empty_sides or 8 in self.empty_sides:
                Color(1, 1, 1, 1)
                Rectangle(pos=(x7, y7), size=(partsize + 1, partsize + 1))
                Color(0, 0, 0, 1)
                if 6 not in self.empty_sides:
                    Line(points=[xa, ya, x8, y8], width=1)
                if 8 not in self.empty_sides:
                    Line(points=[x9, y9, xa, ya], width=1)
                    Color(0.8, 0.8, 0.8, 1)
                    Rectangle(pos=(x7, y7), size=(partsize + 1, partsize))
            if 8 in self.empty_sides:
                Color(1, 1, 1, 1)
                Rectangle(pos=(x9, y9), size=(partsize + 1, 4 * partsize + 1))
                Color(0, 0, 0, 1)
                Line(points=[x2, y2, xa, ya], width=1)

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
