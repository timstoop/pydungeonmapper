from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView


class SmartGridLayout(GridLayout):
    def get_child_index(self, child):
        return self.children.index(child)

    def get_my_neighbours(self, child):
        my_index = self.get_child_index(child)
        neighbours = {}
        neighbours['west'] = self.get_west_neighbour(my_index)
        neighbours['east'] = self.get_east_neighbour(my_index)
        neighbours['north'] = self.get_north_neighbour(my_index)
        neighbours['south'] = self.get_south_neighbour(my_index)
        neighbours['northwest'] = self.get_west_neighbour(neighbours['north'])
        neighbours['northeast'] = self.get_east_neighbour(neighbours['north'])
        neighbours['southwest'] = self.get_west_neighbour(neighbours['south'])
        neighbours['southeast'] = self.get_east_neighbour(neighbours['south'])
        return neighbours

    def get_west_neighbour(self, childidx):
        # The index of the cell to our left is only there if we cannot divide our index + 1 through the number of columns
        if ((childidx + 1) % self.cols) > 0:
            return (childidx + 1)
        else:
            return None

    def get_east_neighbour(self, childidx):
        # The index of the cell to our right is only there if we cannot divide our index through the number of columns
        if (childidx % self.cols) > 0:
            return (childidx - 1)
        else:
            return None

    def get_north_neighbour(self, childidx):
        # The index of the cell above us is only there if our index + cols is not higher than the total number of cols
        if (childidx + self.cols) < (self.cols * self.rows):
            return (childidx + self.cols)
        else:
            return None

    def get_south_neighbour(self, childidx):
        # The index of the cell below us is only there if our index - cols is not less than zero
        if (childidx - self.cols) > 0:
            return (childidx - self.cols)
        else:
            return None

    def get_child_at(self, pos):
        pos = self.to_widget(*pos)
        colwidth = self.width / self.cols
        rowheight = self.height / self.rows
        col = int((self.width - pos[0]) / colwidth)
        row = int(pos[1] / rowheight)
        child = col + (row * self.cols)
        if child > len(self.children):
            # Apparantly, we can get out of the box, fix that.
            child = child - self.cols
        return child

class SmartScrollView(ScrollView):
    def on_touch_down(self, touch):
        if 'button' in touch.profile and touch.button == 'middle':
            return super(SmartScrollView, self).on_touch_down(touch)
        else:
            # This is copied from ScrollView.on_scroll_start(), needed to propagate the other clicks
            touch.apply_transform_2d(self.to_local)
            if self.dispatch_children('on_touch_down', touch):
                return True