from kivy_garden.mapview import MapMarker
from kivy.animation import Animation
# Class for the blinker entity created on the map widget

class GpsBlinker(MapMarker):

    def blink(self):
        # Animation that changes the blink size and opacity
        anim = Animation(outer_opacity=0, blink_size=30)
        # When the animation completes, reset the animation, then repeat
        anim.bind(on_complete=self.reset)
        anim.start(self)

    def reset(self, *args):
        self.outer_opacity = 1
        self.blink_size = self.default_blink_size
        self.blink()

    # blink --> outer_opacity = 0, blink_size = 30
    # reset --> outer_opacity = 1, blink_size = default = 15